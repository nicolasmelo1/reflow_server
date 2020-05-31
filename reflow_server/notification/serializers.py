from reflow_server.notification.models import UserNotification, NotificationConfiguration
from reflow_server.notification.relations import NotificationConfigurationVariableSerializer
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService

from rest_framework import serializers

import re

class UnreadAndReadNotificationSerializer(serializers.ModelSerializer):
    def save(self):
        user_notification = UserNotification.objects.filter(
            user_id=self.context['user_id'], 
            id=self.validated_data['notification_id']
        ).first()
        user_notification.has_read = True
        user_notification.save()


    class Meta:
        fields = ('notification_id', )
        model = UserNotification


class NotificationConfigurationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    notification_configuration_variables = NotificationConfigurationVariableSerializer(many=True)
    text = serializers.CharField()

    def validate_text(self, data):
        data = re.sub(r'{{(\w+)?}}', r'{{}}', data)
        return data


    def validate(self, data):
        self.notification_configuration_service = NotificationConfigurationService(instance=self.instance)
        for variable in data['notification_configuration_variables']:
            self.notification_configuration_service.add_notification_variable(variable['field']['id'], variable['field']['name'])
        try:
            self.notification_configuration_service.validate_notification_configuration(data['text'])
        except:
            raise serializers.ValidationError(detail='invalid_variable')
        return data

    def save(self):
        instance = self.notification_configuration_service.create_or_update(
            self.context['company_id'],
            self.validated_data['for_company'],
            self.validated_data['name'],
            self.validated_data['text'],
            self.validated_data['days_diff'],
            self.validated_data['form'],
            self.validated_data['field'],
            self.context['user_id']
        )

        return instance

    class Meta:
        model = NotificationConfiguration
        # adds custom messages, the default error messages are not that useful, we want the error message to be more "dumb"
        # so the user interface can parse better
        # https://stackoverflow.com/a/26975268/13158385
        extra_kwargs = { field : {'error_messages': {'null': 'blank', 'blank': 'blank'}} for field in ('for_company', 'name', 'text', 'user_id', 'days_diff', 'form', 'field') }
        fields = ('id', 'for_company', 'name', 'text', 'user_id', 'days_diff', 'form', 'field', 'notification_configuration_variables')
