from django.db import models


class ThemePDFTemplateConfigurationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def theme_pdf_template_configurations_by_theme_id(self, theme_id):
        return self.get_queryset().filter(theme_id=theme_id)
    
    def create_theme_pdf_template_configuration(self, theme_id, theme_form_id, name):
        return self.get_queryset().create(
            theme_id=theme_id,
            form_id=theme_form_id,
            name=name
        )