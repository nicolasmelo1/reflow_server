from rest_framework import serializers

from reflow_server.notification.models import UserNotification, NotificationConfiguration
from reflow_server.notification.relations import NotificationConfigurationVariableRelation
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService
from reflow_server.formulary.models import Field

import re


class UnreadAndReadNotificationSerializer(serializers.ModelSerializer):
    """
    Serializer used for updating when the user reads a new notification.
    """
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


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving the notifications of a user. 
    (UserNotification may die in the upcomming future, so you can use Notification instead)
    """
    form_name = serializers.CharField(source='notification.form.form.form_name')
    created_at = serializers.DateTimeField(source='notification.created_at')
    form = serializers.IntegerField(source='notification.form_id')
    notification_id = serializers.IntegerField()
    notification = serializers.CharField(source='notification.notification')

    class Meta:
        model = UserNotification
        fields = '__all__'


class NotificationConfigurationSerializer(serializers.ModelSerializer):
    """
    Serializer used for CRU of NotificationConfigurations. It retrieves objects, creates, and updates
    the NotificationConfiguration. On create or update we also validate to check if everything is valid on
    NotificationConfigurationService. We create and updates inside the service because it contains some business
    logic that needs to be contained inside of the Service class.

    Raises:
        serializers.ValidationError: If the NotificationConfiguration is invalid
    """
    id = serializers.IntegerField(allow_null=True)
    notification_configuration_variables = NotificationConfigurationVariableRelation(many=True)
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
        # so the user interface can parse better https://stackoverflow.com/a/26975268/13158385
        extra_kwargs = { field : {'error_messages': {'null': 'blank', 'blank': 'blank'}} for field in ('for_company', 'name', 'text', 'user_id', 'days_diff', 'form', 'field') }
        fields = ('id', 'for_company', 'name', 'text', 'user_id', 'days_diff', 'form', 'field', 'notification_configuration_variables')


class NotificationFieldsSerializer(serializers.ModelSerializer):
    """
    Serializer used for retriving fields that can be used as variables and fields that can be used on
    NotificationConfiguration. On the second one, we only accept `date` field_types.
    """
    class Meta:
        model = Field
        fields = ('label_name','name', 'id')
