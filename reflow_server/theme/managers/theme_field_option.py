from django.db import models

import uuid


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
            django.db.models.QuerySet(str): Queryset where each item is the option as string.
        """
        return self.get_queryset().filter(field_id=theme_field_id).values_list('option', flat=True)
    
    def create_theme_field_option(self, theme_field_instance, option, order):
        """
        Creates a new ThemeFieldOption instance

        Args:
            theme_field_instance (reflow_server.theme.models.ThemeField): The ThemeField instance that this
                                                                          option is bound to.
            option (str): The option, option is nothing more than a string with a value, this is the option
                          the user can select.
            order (int): The ordering of the options, which comes first and which is last.

        Returns:
            reflow_server.theme.models.ThemeFieldOptions: The newly created theme field option instance.
        """
        return self.get_queryset().create(
            field=theme_field_instance,
            option=option,
            uuid=uuid.uuid4(),
            order=order
        )