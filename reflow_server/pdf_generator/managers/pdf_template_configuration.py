
from django.db import models


class PDFTemplateConfigurationPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def pdf_template_configuration_by_user_id_company_id_and_form_name(self, user_id, company_id, form_name):
        return self.get_queryset().filter(user_id=user_id, company_id=company_id, form__form_name=form_name)