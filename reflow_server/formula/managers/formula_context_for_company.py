from django.db import models


class FormulaContextForCompanyFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def formula_context_for_company_by_company_id(self, company_id):
        return self.get_queryset().filter(company_id=company_id).first() 
        