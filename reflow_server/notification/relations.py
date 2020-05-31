from rest_framework import serializers

from reflow_server.notification.models import NotificationConfigurationVariable


class NotificationConfigurationVariableSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source='field.name', allow_null=True)
    field_id = serializers.IntegerField(source='field.id', allow_null=True)

    class Meta:
        model = NotificationConfigurationVariable
        extra_kwargs = { field : {'error_messages': {'null': 'blank', 'blank': 'blank'}} for field in ('field_id', 'field_name')}
        fields = ('field_id', 'field_name')
