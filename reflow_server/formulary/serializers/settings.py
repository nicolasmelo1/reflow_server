from rest_framework import serializers

from reflow_server.formulary.models import Group, Form, FormType
from reflow_server.formulary.services import FormularyService, GroupService

class FormularyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        formulary_service = FormularyService(user_id=self.context['user_id'], company_id=self.context['company_id'])
        forms = data.filter(id__in=formulary_service.formulary_ids_the_user_has_access_to, depends_on__isnull=True).order_by('order')
        return super(FormularyListSerializer, self).to_representation(forms)

class FormularySerializer(serializers.ModelSerializer):
    """
    Serializer for editing formularies and for loading to be used when loading groups formularies

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
    """
    id = serializers.IntegerField(allow_null=True)
    form_name = serializers.CharField(allow_null=True, allow_blank=True)

    def save(self):
        if self.instance:
            instance = Form
        else:
            instance = self.instance

        formulary_service = FormularyService(user_id=self.context['user_id'], company_id=self.context['company_id'])
        instance = formulary_service.save_formulary(
            instance, 
            self.validated_data['enabled'], 
            self.validated_data['form_name'], 
            self.validated_data['label_name'], 
            self.validated_data['order'], 
            self.validated_data['group']
        )
        return instance
    
    class Meta:
        model = Form
        list_serializer_class = FormularyListSerializer
        fields = ('id', 'label_name', 'form_name', 'enabled', 'group', 'order')


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for editing groups and for loading to be used when loading groups

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
    """
    id = serializers.IntegerField(allow_null=True)
    form_group = FormularySerializer(many=True, required=False, allow_null=True)

    @transaction.atomic
    def update(self, instance, validated_data):
        group_service = GroupService(self.context['user_id'], self.context['company_id'])
        instance = group_service.save_group(
            instance, 
            validated_data['name'],
            validated_data['enabled'],
            validated_data['order']
        )
        return instance

    class Meta:
        model = Group
        fields = ('id', 'name', 'enabled', 'order', 'form_group')
