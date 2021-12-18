from django.db import models


class CompanyBillingDraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def exists_paying_company_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id, is_paying_company=True).exists()
