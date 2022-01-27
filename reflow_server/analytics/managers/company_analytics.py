from django.db import models

class CompanyAnalyticsAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def sector_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id).values_list('sector', flat=True).first()