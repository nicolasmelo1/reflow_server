from django.db import models


class CurrentCompanyChargeNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def quantity_of_permitted_notifications_for_company_id(self, company_id):
        return self.get_queryset().filter(
            individual_charge_value_type__name='per_notification', 
            company_id=company_id
        ).values_list('quantity', flat=True).first()