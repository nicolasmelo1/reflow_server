from django.db import models


class FormPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def formulary_id_by_company_id_and_form_name(self, company_id, form_name):
        return self.get_queryset().filter(company_id=company_id, form_name=form_name)