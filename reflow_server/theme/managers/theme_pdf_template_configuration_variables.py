from django.db import models


class ThemePDFTemplateConfigurationVariablesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def theme_pdf_template_configuration_variables_by_theme_pdf_template_configuration_id(self, theme_pdf_template_configuration_id):
        return self.get_queryset().filter(pdf_template_id=theme_pdf_template_configuration_id)

    def create_theme_pdf_template_configuration_variable(self, theme_pdf_template_configuration_id, theme_field_id):
        return self.get_queryset().create(
            pdf_template_id=theme_pdf_template_configuration_id,
            field_id=theme_field_id
        )