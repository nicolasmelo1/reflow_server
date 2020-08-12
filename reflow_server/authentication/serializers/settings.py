from django.conf import settings

from rest_framework import serializers

from reflow_server.authentication.models import UserExtended, Company
from reflow_server.authentication.relations import OptionAccessedByRelation, FormAccessedByRelation


class CompanySettingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Company
        fields = ('name',) 


class UserSettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    option_accessed_by_user = OptionAccessedByRelation(many=True)
    form_accessed_by_user = FormAccessedByRelation(many=True)
    
    class Meta:
        model = UserExtended
        fields = ('id', 'username', 'first_name', 'last_name', 'profile_id', 'option_accessed_by_user', 'form_accessed_by_user')
        
