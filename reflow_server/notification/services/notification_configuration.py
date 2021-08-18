from django.db import transaction

from reflow_server.core.events import Event
from reflow_server.formulary.models import Field, Form
from reflow_server.authentication.models import UserExtended
from reflow_server.notification.models import NotificationConfiguration, NotificationConfigurationVariable, \
    PreNotification
from reflow_server.notification.services.pre_notification import PreNotificationService

import re


class NotificationConfigurationFieldsService:
    def __init__(self, company_id, form_id):
        """
        Gets the possible fields that can be used in your notification configuration such as the `field_type` as date to be used
        and the possible fields to be used as variable.

        Args:
            form_id (int): must be set if you are trying to get the notification_configuration_fields you could use
            for variables and to be notified.
            company_id (int): must be set if you are trying to get the notification_configuration_fields you could use
            for variables and to be notified.
        """
        self.__fields = Field.objects.filter(
            form__depends_on_id=form_id, 
            form__depends_on__group__company_id=company_id, 
            enabled=True, 
            form__enabled=True, 
            form__depends_on__enabled=True, 
            form__depends_on__group__enabled=True
        )

    @property
    def get_notification_fields(self):
        return self.__fields.filter(type__type='date')

    @property
    def get_variable_fields(self):
        return self.__fields


class NotificationConfigurationService:
    def __init__(self):
        """
        Service used for notification configuration creation and/or update.

        Available Methods:
            .get_notification_configuration_data_from_pre_notifications() -- This method is used when building the notifications.
                                                                             Before building the notifications you first need the 
                                                                             data to effectively build the notifications, thats why 
                                                                             you use this method for.
            .add_notification_variable() -- used for adding notification variables so they can be used for validation and
                                            also on creating or updating notification configurations. If you notification 
                                            configuration has varibles, you must call this function before anything.
            .validate_notification_configuration() -- used for validating the notification configuration, raises error if invalid
            .save_notification_configuration() -- creates or updates the notification configuration based on the instance defined when initializing
                                   the class. 
        """
        self.__variables = list()
    
    def add_notification_variable(self, field_id):
        """
        Method used for adding notification variables so they can be used for validation and
        also on creating or updating notification configurations. If you notification 
        configuration has varibles, you must call this function before anything.

        Arguments:
            field_id {int} -- The id of the field of the notification configuration variable
            field_name {str} -- The name of the field of the notification configuration variable
        """
        self.__variables.append(field_id)

    def validate_notification_configuration(self, notification_text):
        """
        Recieves a notification text and validates if it is valid or not.

        Arguments:
            notification_text {str} -- The text of the notification configuration, refer to 
                                       `reflow_server.notification.models.NotificationConfiguration`
                                       for further reference.

        Raises:
            AssertionError: If your text has variables and you don't call `.add_notification_variable()` for adding
                            the variables before calling this method, this raises an error.
            AssertionError: You variables cannot have empty `ids` or `names`
        """
        variables = len(re.findall(r'{{}}', notification_text))
        if variables != len(self.__variables): 
            raise AssertionError('Use `.add_notification_variable()` method to add all of the variables before '
                                 'calling `.validate_notification_configuration()` function')
        if any([variable in [None, ''] for variable in self.__variables]):
            raise AssertionError('Invalid `id` or invalid `name` in one of the variables, must not be `None` or empty string')

    def __create_or_update_notification_configuration_variables(self, instance):
        """
        Does what the name suggests, based on the variables stored in the list __variables we update each 
        NotificationConfiguration variable model.
        """
        NotificationConfigurationVariable.objects.filter(notification_configuration=instance).delete()
        NotificationConfigurationVariable.objects.bulk_create([
            NotificationConfigurationVariable(
                field_id=notification_configuration_variable_id,
                notification_configuration=instance,
                order=index+1
            ) for index, notification_configuration_variable_id in enumerate(self.__variables)
        ])

    @transaction.atomic
    def save_notification_configuration(self, company_id, for_company, name, text, days_diff, form, field, user_id, instance=None):
        """
        IF YOU WANT TO ADD OR UPDATE VARIABLES YOU MUST ADD VARIABLES FIRST USING THE `.add_variables()` method.
        As the name of the method suggests this method is for creating or updating a certain notification_configuration.
        It's important to understand that after creating or updating the NotificationConfiguration model we also need to
        update it's variables, if it has any, and also update all of the PreNotifications.

        Args:
            company_id (int):  The id of the current company
            for_company (bool): Sets the notification configuration for the hole company 
            name (str): Just a placeholder and user friendly name for the notification configuration, setted by the user
            text (str): The text of the notification configuration, it's important to understand it also could contain variables
                        if that's the case, use `.add_notification_variable()` method to add variables.
            days_diff (int): The number of the difference of days to notify. So you could notify the user on the same day, sixty
                             days earlier of the date, or even sixty days after the date
            form (reflow_server.formulary.models.Form): What form does this notification_configuration references to
            field (reflow_server.formulary.models.Field): What `date` field_type field does this notification configuration 
                                                          references to
            user_id (int): The user id creating this notification configuration 
            instance (reflow_server.notification.models.NotificationConfiguration, optional): The instance to create or update. Defaults to NotificationConfiguration().

        Returns:
            reflow_server.notification.models.NotificationConfiguration: The newly created or updated instance.
        """
        if instance == None:
            instance = NotificationConfiguration()
        
        # if the user is not an admin and is trying to set the for_company, we enforce the for_company on being False
        if for_company and UserExtended.notification_.exists_user_id_excluding_admin(user_id):
            for_company = False

        form_id =  form.id if isinstance(form, Form) else form
        instance, was_created = NotificationConfiguration.objects.update_or_create(
            id=instance.id if instance else None,
            defaults={
                'for_company': for_company,
                'name': name,
                'text': text,
                'days_diff': days_diff,
                'form_id': form_id,
                'field_id': field.id if isinstance(field, Field) else field,
                'user_id': user_id
            }
        )

        self.__create_or_update_notification_configuration_variables(instance)
        PreNotificationService.update(company_id=company_id)

        # Sends events that a new notification was created or updated.
        events_data = {
            'user_id': user_id,
            'company_id': company_id,
            'form_id': form_id,
            'notification_configuration_id': instance.id
        }
        if was_created:
            Event.register_event('notification_configuration_created', events_data)
        else:
            Event.register_event('notification_configuration_updated', events_data)
        return instance

    @staticmethod
    def remove_notification_configuration(user_id, notification_configuration_id):
        """
        Removes a notification configuration

        Arguments:
            user_id {int} -- the id of the user who this notification configuration is to
            notification_configuration_id {int} -- the notification_configuration_id to remove.
        """
        NotificationConfiguration.objects.filter(user_id=user_id, id=notification_configuration_id).delete()

    @staticmethod
    def get_notification_configuration_data_from_pre_notifications(pre_notification_list_ids):
        """
        This method is used when building the notifications. Before building the notifications
        you first need the data to effectively build the notifications, thats why you use this method
        for. You send a pre_notification_list_ids, and it retrieves the data to build each notification
        from each pre_notification. 

        Then the WORKER application uses this data to build the notification for each user.

        Arguments:
            pre_notification_list_ids {list(int)} -- list with pre_notification ids. 

        Returns:
            list(dict) -- List of dicts to be parsed by NotificationDataForBuildSerializer serializer.
        """
        response = list()
        pre_notifications = PreNotification.objects.filter(id__in=pre_notification_list_ids)
        for pre_notification in pre_notifications:
            variable_values = []

            notification_configuration = NotificationConfiguration.objects.filter(id=pre_notification.notification_configuration_id).first()
            notification_configuration_variables = NotificationConfigurationVariable.objects.filter(
                notification_configuration_id=pre_notification.notification_configuration_id
            ).values_list('field_id', flat=True)

            for notification_configuration_variable in notification_configuration_variables:
                form_value = FormValue.notification_.form_value_by_main_formulary_data_id_and_field_id(
                    pre_notification.dynamic_form_id, 
                    notification_configuration_variable
                )
                if form_value:
                    variable_values.append(form_value)
                else:
                    variable_values.append(FormValue(
                        field_id=notification_configuration_variable, 
                        value=''))

            response.append({
                'id': notification_configuration.id,
                'for_company': notification_configuration.for_company,
                'text': notification_configuration.text,
                'pre_notification_id': pre_notification.id,
                'user_id': pre_notification.user_id,
                'form_id': pre_notification.dynamic_form_id,
                'variables': variable_values
            })
        return response
