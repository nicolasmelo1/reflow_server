from django.db import models


class ThemeFieldOptionThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def options_by_theme_field_id(self, theme_field_id):
        """
        Returns a queryset of options, where each option is a string. 
        This queryset holds all of the options of a specific field_id

        Args:
            field_id (int): The id of a single 

        Returns:
            django.db.QuerySet(str): Queryset where each item is the option as string.
        """
        return self.get_queryset().filter(field_id=theme_field_id).values_list('option', flat=True)