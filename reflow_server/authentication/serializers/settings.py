from django.conf import settings

from rest_framework import serializers

from reflow_server.authentication.services.users import UsersService
from reflow_server.authentication.models import UserExtended, Company
from reflow_server.authentication.relations import OptionAccessedByRelation, FormAccessedByRelation, \
    FormularyOptionsRelation
from reflow_server.formulary.models import Group


class CompanySettingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Company
        fields = ('name',) 


class UserSettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    email = serializers.EmailField(allow_blank=False, allow_null=False, error_messages={'invalid': 'invalid', 'blank': 'blank'})
    first_name = serializers.CharField(allow_blank=False, allow_null=False, error_messages={'invalid': 'invalid', 'blank': 'blank'})
    last_name = serializers.CharField(allow_blank=False, allow_null=False, error_messages={'invalid': 'invalid', 'blank': 'blank'})
    option_accessed_by_user = OptionAccessedByRelation(many=True)
    form_accessed_by_user = FormAccessedByRelation(many=True)
    change_password_url = serializers.CharField(default='')

    def validate(self, data):
        user_id = self.instance.id if self.instance else None
        if UserExtended.objects.filter(username=data.get('email')).exclude(id=user_id).exists():
            raise serializers.ValidationError(detail={'detail': 'email', 'reason': 'must_be_unique'})
        if not data.get('profile', None):
            raise serializers.ValidationError(detail={'detail': 'profile', 'reason': 'invalid_profile'})
        return data

    def save(self, company_id):
        self.company_id = company_id
        super(UserSettingsSerializer, self).save()

    def create(self, validated_data):
        users_service = UsersService(self.company_id)   
        return users_service.create( 
            validated_data.get('email'),
            validated_data.get('first_name'),
            validated_data.get('last_name'),
            validated_data.get('profile'),
            [option_accessed_by_user['field_option_id'] for option_accessed_by_user in validated_data.get('option_accessed_by_user', [])],
            [form_accessed_by_user['form_id'] for form_accessed_by_user in validated_data.get('form_accessed_by_user', [])],
            validated_data.get('change_password_url')
        )

    def update(self, instance, validated_data):
        users_service = UsersService(self.company_id)
        return users_service.update(
            instance.id, 
            validated_data.get('email'),
            validated_data.get('first_name'),
            validated_data.get('last_name'),
            validated_data.get('profile'),
            [option_accessed_by_user['field_option_id'] for option_accessed_by_user in validated_data.get('option_accessed_by_user', [])],
            [form_accessed_by_user['form_id'] for form_accessed_by_user in validated_data.get('form_accessed_by_user', [])]
        )

    class Meta:
        model = UserExtended
        fields = ('id', 'email', 'first_name', 'last_name', 'profile', 'option_accessed_by_user', 'form_accessed_by_user', 'change_password_url')
    

class FormularyAndFieldOptionsSerializer(serializers.ModelSerializer):
    form_group = FormularyOptionsRelation(many=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'enabled', 'form_group')
