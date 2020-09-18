from django.db import models


class ThemeFieldThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_fields_by_theme_id(self, theme_id):
        """
        Returns a queryset of ThemeField instances based on a theme_id

        Args:
            theme_id (int): The id of the Theme instance of where this ThemeField is from.

        Returns:
            django.db.QuerySet(reflow_server.theme.models.ThemeField): A queryset of ThemeField instances
            from the theme_id
        """
        return self.get_queryset().filter(form__depends_on__theme_id=theme_id)
