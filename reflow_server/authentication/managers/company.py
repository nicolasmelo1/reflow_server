from django.db import models


class CompanyAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def company_by_company_id(self, company_id):
        return self.get_queryset().filter(id=company_id).first()
    
    def company_by_endpoint(self, endpoint):
        return self.get_queryset().filter(endpoint=endpoint).first()