from django.conf import settings

from rest_framework import serializers

from reflow_server.authentication.services.users import UsersService
from reflow_server.authentication.services.company import CompanyService
from reflow_server.authentication.models import UserExtended, Company
from reflow_server.authentication.relations import OptionAccessedByRelation, FormAccessedByRelation, \
    FormularyOptionsRelation
from reflow_server.formulary.models import Group


class CompanySettingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(allow_blank=False, allow_null=False, error_messages={'invalid': 'invalid', 'blank': 'blank'})
    logo_image_url = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    
    def __init__(self, *args, **kwargs):
        self.company_service = CompanyService()
        super(CompanySettingsSerializer, self).__init__(*args, **kwargs)

    def save(self, files=None):
        if self.instance is not None:
            instance = self.update(self.instance, self.validated_data, files)
        else:
            instance = self.create(self.validated_data)

        return instance

    def update(self, instance, validated_data, files):
        company_logo = list(files.values())[0] if files and isinstance(files, dict) else None
        instance = self.company_service.update_company(
            company_id=instance.id, 
            name=validated_data.get('name', instance.name),
            company_logo=company_logo
        )
        return instance

    

    class Meta:
        model = Company
        fields = ('name', 'logo_image_url') 


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
        if UserExtended.authentication_.exists_user_by_email_excluding_id(data.get('email'), user_id):
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
