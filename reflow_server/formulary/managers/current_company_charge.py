from django.db import models


class CurrentCompanyChargeFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def quantity_of_per_page_permission_for_company_id(self, company_id):
        return self.get_queryset().filter(
            company_id=company_id, 
            individual_charge_value_type__name='per_page'
        ).order_by(
            '-quantity'
        ).values_list(
            'quantity', flat=True
        ).first()

    def quantity_of_per_formula_fields_permission_for_company_id(self, company_id):
        return self.get_queryset().filter(
            company_id=company_id, 
            individual_charge_value_type__name='per_formula_fields'
        ).order_by(
            '-quantity'
        ).values_list(
            'quantity', flat=True
        ).first()
