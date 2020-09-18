from django.db import models


class ThemeThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def themes_by_company_type_name(self, company_type_name):
        return self.get_queryset().filter(company_type__name=company_type_name)

    def theme_by_theme_id(self, theme_id):
        """
        Retrives a single Theme instance by the theme id

        Args:
            theme_id (int): The Theme instance id to retrieve

        Returns:
            reflow_server.theme.models.Theme: The Theme instance retrieved by its id.
        """
        return self.get_queryset().filter(id=theme_id).first()