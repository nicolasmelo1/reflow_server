from django.db import models


class CurrentCompanyChargeBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def quantity_by_company_id_and_individual_charge_value_type_name(self, company_id, individual_charge_value_type_name):
        return self.get_queryset().filter(company_id=company_id, individual_charge_value_type__name=individual_charge_value_type_name).values_list('quantity', flat=True).first()