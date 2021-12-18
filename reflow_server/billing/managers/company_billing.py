from django.db import models

class CompanyBillingBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def plan_id_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id).values_list('plan_id', flat=True).first()
        
    def company_id_by_vindi_client_id(self, vindi_client_id):
        return self.get_queryset().filter(vindi_client_id=vindi_client_id).values_list('company_id', flat=True).first()

    def exists_paying_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id, is_paying_company=True).exists()

    def exists_super_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id, is_supercompany=True).exists()