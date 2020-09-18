from django.db import models


class ThemeNotificationConfigurationVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_notification_configuration_variables_by_notification_configuration_id_ordered(self, notification_configuration_id):
        return self.get_queryset().filter(notification_configuration_id=notification_configuration_id).order_by('order')