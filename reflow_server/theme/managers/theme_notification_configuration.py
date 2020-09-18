from django.db import models


class ThemeNotificationConfigurationThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_notification_configurations_by_theme_id(self, theme_id):
        return self.get_queryset().filter(field__form__depends_on__theme_id=theme_id)