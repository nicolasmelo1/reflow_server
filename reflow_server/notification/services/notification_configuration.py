from django.db import transaction

from reflow_server.authentication.models import UserExtended
from reflow_server.notification.models import NotificationConfiguration, NotificationConfigurationVariable
from reflow_server.notification.services.pre_notification import PreNotificationService

import re

class NotificationVariables:
    def __init__(self, field_id, field_name):
        """
        Simple class used for holding notification variable information

        Arguments:
            field_id {int} -- The id of the field of the notification configuration variable
            field_name {str} -- The name of the field of the notification configuration variable
        """
        self.name = field_name
        self.id = field_id


class NotificationConfigurationService:
    def __init__(self, instance=None):
        """
        Service used for notification configuration creation and/or update.

        Available Methods:
            .add_notification_variable() -- used for adding notification variables so they can be used for validation and
                                            also on creating or updating notification configurations. If you notification 
                                            configuration has varibles, you must call this function before anything.
            .validate_notification_configuration() -- used for validating the notification configuration, raises error if invalid
            .create_or_update() -- creates or updates the notification configuration based on the instance defined when initializing
                                   the class. 

        Keyword Arguments:
            instance {reflow_server.notification.models.NotificationConfiguration} -- If you are trying to update an 
            NotificationConfiguration instance you must set use this variable. Works like serializer Instances. (default: {None})
        """
        self.instance = instance
        self.__variables = list()
    
    def add_notification_variable(self, field_id, field_name):
        """
        Method used for adding notification variables so they can be used for validation and
        also on creating or updating notification configurations. If you notification 
        configuration has varibles, you must call this function before anything.

        Arguments:
            field_id {int} -- The id of the field of the notification configuration variable
            field_name {str} -- The name of the field of the notification configuration variable
        """
        self.__variables.append(NotificationVariables(field_id, field_name))

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
        if any([variable.id in [None, ''] and variable.name in [None, ''] for variable in self.__variables]):
            raise AssertionError('Invalid `id` or invalid `name` in one of the variables, must not be `None` or empty string')

    def __create_or_update_notification_configuration_variables(self):
        """
        Does what the name suggests, based on the variables stored in the list __variables we update each 
        NotificationConfiguration variable model.
        """
        NotificationConfigurationVariable.objects.filter(notification_configuration=self.instance).delete()
        update_notification_configuration_variable_ids = []
        NotificationConfigurationVariable.objects.bulk_create([
            NotificationConfigurationVariable(
                field_id=notification_configuration_variable.id,
                notification_configuration=instance,
                order=index+1
            ) for index, notification_configuration_variable in enumerate(self.__variables)
        ])


    def __create(self, for_company, name, text, days_diff, form, field, user_id):
        instance = NotificationConfiguration.objects.create(
            for_company=for_company,
            name=name,
            text=text,
            days_diff=days_diff,
            form=form,
            field=field,
            user_id=user_id
        )
        return instance
    
    def __update(self, for_company, name, text, days_diff, form, field, user_id):
        self.instance.for_company = for_company
        self.instance.name = name
        self.instance.text = text
        self.instance.days_diff = days_diff
        self.instance.form = form
        self.instance.field = field
        self.instance.user = user_id
        self.instance.save()

        return self.instance

    @transaction.atomic
    def create_or_update(self, company_id, for_company, name, text, days_diff, form, field, user_id):
        """
        As the name of the method suggests this method is for creating or updating a certain notification_configuration.
        It's important to understand that after creating or updating the NotificationConfiguration model we also need to
        update it's variables, if it has any, and also update all of the PreNotifications.

        Arguments:
            company_id {int} -- The id of the current company
            for_company {bool} -- Sets the notification configuration for the hole company 
            name {str} -- Just a placeholder and user friendly name for the notification configuration, setted by the user
            text {str} -- The text of the notification configuration, it's important to understand it also could contain variables
                          if that's the case, use `.add_notification_variable()` method to add variables.
            days_diff {int} -- The number of the difference of days to notify. So you could notify the user on the same day, sixty
                               days earlier of the date, or even sixty days after the date
            form {reflow_server.formulary.models.Form} -- What form does this notification_configuration references to
            field {reflow_server.formulary.models.Field} -- What `date` field_type field does this notification configuration 
                                                            references to
            user_id {int} -- the user id creating this notification configuration 

        Returns:
            reflow_server.notification.models.NotificationConfiguration -- The newly created or updated instance.
        """

        # if the user is not an admin and is trying to set the for_company, we enforce the for_company on being False
        if for_company and UserExtended.object.filter(id=user_id).excludes(profile__name='admin').exists():
            for_company = False
        
        if self.instance:
            instance = self.__update(for_company, name, text, days_diff, form, field, user_id)
        else:
            instance = self.__create(for_company, name, text, days_diff, form, field, user_id)

        self.__create_or_update_notification_configuration_variables()
        PreNotificationService.update(company_id, notification_configuration_id=instance.id)
        return instance
