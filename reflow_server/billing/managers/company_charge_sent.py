from django.db import models


class CompanyChargeSentBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_company_charge_sent(self, company_id, total_value):
        return self.get_queryset().create(
            company_id=company_id,
            total_value=total_value
        )