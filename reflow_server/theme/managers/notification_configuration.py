from django.db import models


class NotificationConfigurationThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def notification_configurations_for_company_by_user_id_company_id_and_main_form_ids(self, user_id, company_id, main_form_ids):
        return self.get_queryset().filter(field__form__depends_on__group__company_id=company_id, user_id=user_id, field__form__in=main_form_ids, for_company=True)