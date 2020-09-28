from django.db import models


class NotificationConfigurationVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()