from django.db import models


class PDFTemplateConfigurationThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def pdf_template_configuration_by_form_ids_company_id_and_user_id(self, form_ids, company_id, user_id):
        return self.get_queryset().filter(form_id__in=form_ids, company_id=company_id, user_id=user_id)