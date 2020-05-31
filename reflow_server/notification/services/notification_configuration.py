from django.db import transaction

from reflow_server.notification.models import NotificationConfiguration, NotificationConfigurationVariable
from reflow_server.notification.services.pre_notification import PreNotificationService

import re

class NotificationVariables:
    def __init__(self, field_id, field_name):
        self.name = field_name
        self.id = field_id


class NotificationConfigurationService:
    def __init__(self, instance=None):
        self.instance = instance
        self.__variables = list()
    
    def add_notification_variable(self, field_id, field_name):
        self.__variables.append(NotificationVariables(field_id, field_name))

    def validate_notification_configuration(self, notification_text):
        variables = len(re.findall(r'{{}}', notification_text))
        if variables != len(self.__variables): 
            raise AssertionError('Use `.add_notification_variable()` method to add all of the variables before '
                                 'calling `.validate_notification_configuration()` function')
        if any([variable.id in [None, ''] and variable.name in [None, ''] for variable in self.__variables]):
            raise AssertionError('Invalid `id` or invalid `name` in one of the variables, must not be `None` or empty string')

    def __create_or_update_notification_configuration_variables(self):
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
        if self.instance:
            instance = self.__update(for_company, name, text, days_diff, form, field, user_id)
        else:
            instance = self.__create(for_company, name, text, days_diff, form, field, user_id)

        self.__create_or_update_notification_configuration_variables()
        PreNotificationService.update(company_id, notification_configuration_id=instance.id)
        return instance
