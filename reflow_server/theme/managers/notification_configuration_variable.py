from django.db import models


class NotificationConfigurationVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def notification_configuration_variables_by_notification_configuration_id_ordered_by_order(self, notification_configuration_id):
        """
        Retrieves the NotificationConfigurationVariable instances of a notification_configuration_id.
        The ordering here is EXTREMELY important

        Args:
            notification_configuration_id (int): A NotificationConfiguration instance id

        Returns:
            django.db.models.QuerySet(reflow_server.notification.models.NotificationConfigurationVariable): A
            Queryset of ORDERED by order NotificationConfigurationVariable instances of a notification_configuration
        """
        return self.get_queryset().filter(notification_configuration=notification_configuration_id).order_by('order')
