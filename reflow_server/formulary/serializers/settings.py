from rest_framework import serializers

from reflow_server.formulary.models import Group, Form, Field, FieldOptions, FieldType
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.group import GroupService
from reflow_server.formulary.services.sections import SectionService
from reflow_server.formulary.services.fields import FieldService


class FieldOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    
    class Meta:
        model = FieldOptions
        fields = ('id', 'option',)


class FieldAsOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    form_depends_on_id = serializers.IntegerField(source='form.depends_on_id', required=False, allow_null=True)
    form_depends_on_group_id = serializers.IntegerField(source='form.depends_on.group_id', required=False, allow_null=True)

    class Meta:
        model = Field
        fields = ('id', 'form_depends_on_id', 'form_depends_on_group_id')


class FieldSerializer(serializers.ModelSerializer):
    """
    Serializer for editing fields and to be used when loading as the child of a section.

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
        form_id (int): the form_id for which form does this field references to (it is the MAIN FORM not section_id).
    """
    id = serializers.IntegerField(allow_null=True)
    field_option = FieldOptionSerializer(many=True)
    form_field_as_option = FieldAsOptionSerializer(allow_null=True)
    name = serializers.CharField(allow_blank=True, allow_null=True)

    def validate_form_field_as_option(self, value):
        if hasattr(self, 'initial_data') and 'type' in self.initial_data and self.initial_data['type']:
            field_type = FieldType.objects.filter(id=self.initial_data['type']).first()
            if field_type and field_type.type == 'form' and (not value or not value['id'] or not value['form']['depends_on_id'] or not value['form']['depends_on']['group_id']):
                raise serializers.ValidationError(detail={'detail': 'form fields must have a connection', 'reason': 'form_fields_connection'})
        return value
    
    def validate_field_option(self, value): 
        if hasattr(self, 'initial_data') and 'type' in self.initial_data and self.initial_data['type']:
            field_type = FieldType.objects.filter(id=self.initial_data['type']).first()
            if field_type and field_type.type in ['option', 'multi_option'] and len(value) == 0:
                raise serializers.ValidationError(detail={'detail': 'option field must have a option', 'reason': 'option_field_empty_option'})
        return value


    def save(self):
        if self.instance:
            instance = self.instance
        else:
            instance = self.Meta.model()

        if (
            self.validated_data.get('form_field_as_option', None) 
            and self.validated_data['form_field_as_option'].get('id', None)
            and self.validated_data['form_field_as_option'].get('form', None)
            and self.validated_data['form_field_as_option']['form'].get('depends_on_id', None)
        ):
            form_field_as_option = Field.objects.filter(
                id=self.validated_data['form_field_as_option']['id'],
                form__depends_on_id=self.validated_data['form_field_as_option']['form']['depends_on_id'],
                form__company_id=self.context['company_id']
            ).first()
        else:
            form_field_as_option = None

        formula_configuration = self.validated_data['formula_configuration'] if self.validated_data.get('formula_configuration', None) not in [None, ''] else None 

        field_service = FieldService(
            user_id=self.context['user_id'], 
            company_id=self.context['company_id'], 
            form_id=self.context['form_id']
        )
        instance = field_service.save_field(
            instance, 
            enabled=self.validated_data['enabled'],
            label_name=self.validated_data['label_name'],
            order=self.validated_data['order'],
            is_unique=self.validated_data['is_unique'],
            field_is_hidden=self.validated_data['field_is_hidden'],
            label_is_hidden=self.validated_data['label_is_hidden'],
            placeholder=self.validated_data.get('placeholder', None),
            required=self.validated_data['required'],
            section=self.validated_data['form'],
            form_field_as_option=form_field_as_option,
            formula_configuration=formula_configuration,
            date_configuration_auto_create=self.validated_data['date_configuration_auto_create'],
            date_configuration_auto_update=self.validated_data['date_configuration_auto_update'],
            number_configuration_number_format_type=self.validated_data.get('number_configuration_number_format_type', None),
            date_configuration_date_format_type=self.validated_data.get('date_configuration_date_format_type', None),
            period_configuration_period_interval_type=self.validated_data.get('period_configuration_period_interval_type', None),
            field_type=self.validated_data['type'],
            field_options=[field_option['option'] for field_option in self.validated_data.get('field_option', list())]
        )
        print(instance)
        return instance

    class Meta:
        model = Field
        exclude = ('created_at', 'updated_at')


class SectionSerializer(serializers.ModelSerializer):
    """
    Serializer for editing sections and to be used when loading as the child of a formulary.

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
        form_id (int): the form_id for which form does this section references to.
    """
    id = serializers.IntegerField(allow_null=True)
    form_name = serializers.CharField(allow_blank=True, allow_null=True)
    form_fields = FieldSerializer(many=True, required=False, allow_null=True)

    def save(self):
        if self.instance:
            instance = self.instance
        else:
            instance = self.Meta.model()

        section_service = SectionService(
            user_id=self.context['user_id'], 
            company_id=self.context['company_id'], 
            form_id=self.context['form_id']
        )
        instance = section_service.save_section(
            instance, 
            enabled=self.validated_data['enabled'],
            label_name=self.validated_data['label_name'],
            order=self.validated_data['order'],
            conditional_value=self.validated_data['conditional_value'] if self.validated_data.get('conditional_value', None) and self.validated_data['conditional_value'] != '' else None,
            section_type=self.validated_data['type'],
            conditional_type=self.validated_data.get('conditional_type', None),
            conditional_on_field=self.validated_data.get('conditional_on_field', None)
        )
        return instance

    class Meta:
        model = Form
        exclude = ('company', 'depends_on', 'created_at', 'updated_at')


class FormularyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        formulary_service = FormularyService(user_id=self.context['user_id'], company_id=self.context['company_id'])
        forms = data.filter(id__in=formulary_service.formulary_ids_the_user_has_access_to, depends_on__isnull=True).order_by('order')
        return super(FormularyListSerializer, self).to_representation(forms)

class FormularySerializer(serializers.ModelSerializer):
    """
    Serializer for editing formularies and for loading to be used when loading groups formularies

    Args:
        is_loading_sections (bool, optional): Set this to true if you want to load the sections when you load the serializer. 
                                              Defaults to False.

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
    """
    id = serializers.IntegerField(allow_null=True)
    form_name = serializers.CharField(allow_null=True, allow_blank=True)
    depends_on_form = SectionSerializer(many=True, required=False, allow_null=True)

    def __init__(self, is_loading_sections=False, *args, **kwargs):
        super(FormularySerializer, self).__init__(*args, **kwargs)
        if not is_loading_sections:
            self.fields.pop('depends_on_form')

    def save(self):
        if self.instance:
            instance = self.instance
        else:
            instance = self.Meta.model()

        formulary_service = FormularyService(user_id=self.context['user_id'], company_id=self.context['company_id'])
        instance = formulary_service.save_formulary(
            instance=instance, 
            enabled=self.validated_data['enabled'], 
            label_name=self.validated_data['label_name'], 
            order=self.validated_data['order'], 
            group=self.validated_data['group']
        )
        return instance
    
    class Meta:
        model = Form
        list_serializer_class = FormularyListSerializer
        fields = ('id', 'label_name', 'form_name', 'enabled', 'group', 'order', 'depends_on_form')


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for editing groups and for loading to be used when loading groups

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
    """
    id = serializers.IntegerField(allow_null=True)
    form_group = FormularySerializer(many=True, required=False, allow_null=True)

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
