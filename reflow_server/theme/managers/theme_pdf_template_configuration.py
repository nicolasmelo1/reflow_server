from django.db import models


class ThemePDFTemplateConfigurationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
