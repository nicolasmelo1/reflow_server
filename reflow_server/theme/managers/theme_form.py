from django.db import models


class ThemeFormThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def main_theme_forms_by_theme_id(self, theme_id):
        """
        Gets a queryset of main_forms, this means ThemeForm instances where depends_on is null.

        Args:
            theme_id (int): The id of the Theme instance of where this ThemeForm is from.

        Returns:
            django.db.QuerySet(reflow_server.theme.models.ThemeForm): A queryset of ThemeForm instances
        """
        return self.get_queryset().filter(theme_id=theme_id, depends_on__isnull=True)

    def sections_theme_forms_by_theme_id(self, theme_id):
        """
        Get queryset of sections of ThemeForm. Remember that sections are the ThemeForm with depends_on
        that equals NULL

        Args:
            theme_id (int): The id of the Theme instance of where this ThemeForm is from.

        Returns:
            django.db.QuerySet(reflow_server.theme.models.ThemeForm): A queryset of ThemeForm instances
        """
        return self.get_queryset().filter(theme_id=theme_id, depends_on__isnull=False)
