from django.db import models


class CurrentCompanyChargePDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def quantity_of_per_charts_permission_for_company_id(self, company_id):
        return self.get_queryset().filter(
            company_id=company_id, 
            individual_charge_value_type__name='per_pdf_download'
        ).order_by(
            '-quantity'
        ).values_list(
            'quantity', flat=True
        ).first()
        