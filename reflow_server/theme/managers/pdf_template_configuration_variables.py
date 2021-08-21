from django.db import models


class PDFTemplateConfigurationVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def pdf_template_configuration_variables_by_pdf_template_configuration_id(self, pdf_template_configuration_id):
        return self.get_queryset().filter(pdf_template_id=pdf_template_configuration_id)