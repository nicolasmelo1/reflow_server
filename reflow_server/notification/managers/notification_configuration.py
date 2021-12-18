from django.db import models


class NotificationConfigurationNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def number_of_notifications_by_user_and_company(self, user_id, company_id):
        return self.get_queryset().filter(user_id=user_id, form__group__company_id=company_id).count()