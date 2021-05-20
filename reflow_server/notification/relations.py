from rest_framework import serializers

from reflow_server.data.models import FormValue
from reflow_server.formulary.models import Field
from reflow_server.notification.models import NotificationConfigurationVariable
from reflow_server.core.relations import ValueField


class NotificationConfigurationVariableRelation(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.name', allow_null=True)
    field_id = serializers.IntegerField(source='field.id', allow_null=True)

    class Meta:
        model = NotificationConfigurationVariable
        extra_kwargs = { field : {'error_messages': {'null': 'blank', 'blank': 'blank'}} for field in ('field_id', 'field_name')}
        fields = ('field_id', 'field_name')


class NotificationConfigurationFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = Field
        fields = ('label_name','name', 'id')


class NotificationFormValueVariableDataForBuildRelation(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.name')
    value = ValueField(source='id')

    class Meta:
        model = FormValue
        fields = ('field_name', 'value')