from django.db import models


class DiscountByIndividualNameForCompanyBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create(self, individual_charge_value_type_id, value, name, company_id):
        instance = self.get_queryset().create(
            individual_charge_value_type_id=individual_charge_value_type_id,
            value=value,
            name=name,
            company_id=company_id
        )
        return instance