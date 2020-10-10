from django.db import models


class ThemeNotificationConfigurationVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_notification_configuration_variables_by_notification_configuration_id_ordered(self, theme_notification_configuration_id):
        """
        Gets a queryset of ORDERED ThemeNotificationConfigurationVariable instances. The order is based on the 
        'order' column. We get the variables from a ThemeNotificationConfiguration instance id.

        Args:
            theme_notification_configuration_id (int): A ThemeNotificationConfiguration instance id

        Returns:
            django.db.models.QuerySet(reflow_server.theme.models.ThemeNotificationConfigurationVariable): A queryset of ORDERED
            ThemeNotificationConfigurationVariable instances
        """
        return self.get_queryset().filter(notification_configuration_id=theme_notification_configuration_id).order_by('order')

    def create_theme_notification_configuration_variable(self, order, theme_notification_configuration_id, theme_field_id):
        """
        Creates a new ThemeNotificationConfigurationVariable instance

        Args:
            order (int): The ordering of the notification variable. The ordering here is EXTREMELY important
            theme_notification_configuration_id (int): A ThemeNotificationConfiguration instance id
            theme_field_id (int): A ThemeField instance id

        Returns:
            reflow_server.theme.models.ThemeNotificationConfigurationVariable: The created 
            ThemeNotificationConfigurationVariable instance
        """
        return self.get_queryset().create(
            order=order,
            notification_configuration_id=theme_notification_configuration_id,
            field_id=theme_field_id
        )
