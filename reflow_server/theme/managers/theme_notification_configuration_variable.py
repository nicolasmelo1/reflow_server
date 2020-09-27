from django.db import models


class ThemeNotificationConfigurationVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_notification_configuration_variables_by_notification_configuration_id_ordered(self, theme_notification_configuration_id):
        """
        Gets a queryset of ORDERED ThemeNotificationConfigurationVariable instances. The order is based on the 
        `order` column. We get the variables from a ThemeNotificationConfiguration instance id.

        Args:
            notification_configuration_id (int): A ThemeNotificationConfiguration instance id

        Returns:
            django.db.QuerySet(reflow_server.theme.models.ThemeNotificationConfigurationVariable): A queryset of ORDERED
            ThemeNotificationConfigurationVariable instances
        """
        return self.get_queryset().filter(notification_configuration_id=theme_notification_configuration_id).order_by('order')