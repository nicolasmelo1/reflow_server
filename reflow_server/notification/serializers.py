from rest_framework import serializers

from reflow_server.core.utils.asynchronous import RunAsyncFunction
from reflow_server.notification.models import UserNotification, NotificationConfiguration, PreNotification, Notification
from reflow_server.notification.relations import NotificationConfigurationVariableRelation, NotificationFormValueVariableDataForBuildRelation, \
    NotificationConfigurationFieldsRelation
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService, \
    NotificationConfigurationFieldsService
from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.notification.services.notification import NotificationService
from reflow_server.formulary.models import Field

import re
import time

class UnreadAndReadNotificationSerializer(serializers.ModelSerializer):
    notification_id = serializers.IntegerField()
    """
    Serializer used for updating when the user reads a new notification.
    """
    def save(self):
        UserNotification.objects.filter(
            user_id=self.context['user_id'], 
            id=self.validated_data['notification_id']
        ).update(
            has_read=True
        )

    class Meta:
        fields = ('notification_id', )
        model = UserNotification


class UserNotificationSerializer(serializers.ModelSerializer):
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
    Serializer used for Create/Read/Update of NotificationConfigurations. It retrieves objects, creates, and updates
    the NotificationConfiguration. On create or update we also validate to check if everything is valid on
    NotificationConfigurationService. We create and updates inside the service because it contains some business
    logic that needs to be contained inside of the Service class.

    Obligatory Context Data:
        company_id (int) -- id of the company
        user_id (int) -- the id of the user

    Raises:
        serializers.ValidationError: If the NotificationConfiguration is invalid
    """
    id = serializers.IntegerField(allow_null=True, required=False)
    notification_configuration_variables = NotificationConfigurationVariableRelation(many=True)
    text = serializers.CharField()

    def validate_text(self, data):
        data = re.sub(r'{{(\w+)?}}', r'{{}}', data)
        return data

    def validate(self, data):
        self.notification_configuration_service = NotificationConfigurationService()
        for variable in data['notification_configuration_variables']:
            self.notification_configuration_service.add_notification_variable(variable['field']['id'])
        try:
            self.notification_configuration_service.validate_notification_configuration(data['text'])
        except:
            raise serializers.ValidationError(detail='invalid_variable')
        return data

    def save(self):
        instance = self.notification_configuration_service.save_notification_configuration(
            self.context['company_id'],
            self.validated_data['for_company'],
            self.validated_data['name'],
            self.validated_data['text'],
            self.validated_data['days_diff'],
            self.validated_data['form'],
            self.validated_data['field'],
            self.context['user_id'],
            instance=self.instance if self.instance else None
        )
        return instance

    class Meta:
        model = NotificationConfiguration
        # adds custom messages, the default error messages are not that useful, we want the error message to be more "dumb"
        # so the user interface can parse better https://stackoverflow.com/a/26975268/13158385
        extra_kwargs = { field : {'error_messages': {'null': 'blank', 'blank': 'blank'}} for field in ('for_company', 'name', 'text', 'user_id', 'days_diff', 'form', 'field') }
        fields = ('id', 'for_company', 'name', 'text', 'user_id', 'days_diff', 'form', 'field', 'notification_configuration_variables')


class NotificationConfigurationFieldsSerializer(serializers.Serializer):
    notification_fields = NotificationConfigurationFieldsRelation(many=True)
    variable_fields = NotificationConfigurationFieldsRelation(many=True)
    
    def __init__(self, form_id, company_id, *args, **kwargs):
        """ 
        Serializer used for retriving fields that can be used as variables and fields that can be used on
        NotificationConfiguration. On the second one, we only accept `date` field_types.


        Args:
            form_id (int): must be set if you are trying to get the notification_configuration_fields you could use
            for variables and to be notified.
            company_id (int): must be set if you are trying to get the notification_configuration_fields you could use
            for variables and to be notified.
        """
        self.notification_configuration_fields_service = NotificationConfigurationFieldsService(company_id, form_id)

        kwargs['data'] = {
            'notification_fields': self.get_notification_fields,
            'variable_fields': self.get_variable_fields
        }
        super(NotificationConfigurationFieldsSerializer, self).__init__(**kwargs)
        self.is_valid()

    @property
    def get_notification_fields(self):
        # this can be more verbose, but it's better to do this way, so our service don't need to know anything about the serializer
        # it just gives us the data that we need
        return NotificationConfigurationFieldsRelation(instance=self.notification_configuration_fields_service.get_notification_fields, many=True).data

    @property
    def get_variable_fields(self):
        # this can be more verbose, but it's better to do this way, so our service don't need to know anything about the serializer
        return NotificationConfigurationFieldsRelation(instance=self.notification_configuration_fields_service.get_variable_fields, many=True).data


class PreNotificationIdsForBuildSerializer(serializers.Serializer):
    pre_notification_ids = serializers.ListField()

    def save(self):
        return NotificationConfigurationService.get_notification_configuration_data_from_pre_notifications(self.validated_data['pre_notification_ids'])


class PreNotificationSerializer(serializers.ModelSerializer):
    dynamic_form_id = serializers.IntegerField(allow_null=True)
    user_id = serializers.IntegerField(allow_null=True)
    notification_configuration_id = serializers.IntegerField(allow_null=True)

    def save(self, *args):
        pre_notification_service = PreNotificationService()     
        async_task = RunAsyncFunction(pre_notification_service.update_from_request)
        async_task.delay(company_id=self.context['company'])

    class Meta:
        model = PreNotification
        fields = ('user_id', 'dynamic_form_id', 'notification_configuration_id')


class NotificationDataForBuildSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    for_company = serializers.BooleanField()
    text = serializers.CharField()
    pre_notification_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    form_id = serializers.IntegerField()
    variables = NotificationFormValueVariableDataForBuildRelation(many=True)


class NotificationListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        notification_service = NotificationService()
        [notification_service.add_notification(
            pre_notification_id=notification['pre_notification_id'],
            notification_text=notification['notification'],
            notification_configuration_id=notification['notification_configuration_id'],
            dynamic_form_id=notification['form_id'],
            user_id=notification['user_id']
        ) for notification in validated_data]
        created_notifications = notification_service.create_notifications()
        return created_notifications

class NotificationSerializer(serializers.ModelSerializer):
    notification = serializers.CharField()
    pre_notification_id = serializers.IntegerField()
    notification_configuration_id = serializers.IntegerField()
    form_id = serializers.IntegerField()
    user_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Notification
        list_serializer_class = NotificationListSerializer
        fields = ('notification', 'pre_notification_id', 'notification_configuration_id', 'form_id', 'user_id')
