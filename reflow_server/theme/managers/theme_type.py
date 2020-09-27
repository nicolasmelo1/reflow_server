from django.db import models


class ThemeTypeThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def exists_theme_type_by_theme_type_id(self, theme_type_id):
        """
        Check if a specific theme_type_id exists

        Args:
            theme_type_id (int): The ThemeType instance id

        Returns:
            bool: returns True if the ThemeType exists or False if the ThemeType does not exists
        """
        return self.get_queryset().filter(id=theme_type_id).exists()

    def empty_theme_type_id(self):
        """
        Returns the id of the 'empty' ThemeType. We have many theme types but empty is like the default.

        Returns:
            int: The id of the ThemeType instance that has the `empty` name.
        """
        return self.get_queryset().filter(name='empty').values_list('id', flat=True).first()