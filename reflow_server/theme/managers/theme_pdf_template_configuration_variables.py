from django.db import models


class ThemePDFTemplateConfigurationVariablesManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    