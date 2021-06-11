from django.db import models


class ThemeFormulaVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_theme_formula_variable(self, theme_field_id, theme_field_variable_id):
        """
        Creates a new ThemeFormulaVarible instance.

        Args:
            theme_field_id (int): A ThemeField instance id
            theme_field_variable_id (int): A ThemeField instance id

        Returns:
            reflow_server.theme.models.ThemeFormulaVariable: The newly created ThemeFormulaVariable instance
        """
        return self.get_queryset().create(
            field_id=theme_field_id,
            variable_id=theme_field_variable_id
        )

    def variable_ids_by_theme_field_id(self, theme_field_id):
        """
        Retrieves all of the formula variable ids by the field_id

        Args:
            theme_field_id (int): The ThemeField instance id to retrieve the variables for

        Returns:
            django.db.models.QuerySet(int): A QuerySet of ThemeField instance ids, which are variables of a formula.
        """
        return self.get_queryset().filter(field_id=theme_field_id).values_list('variable_id', flat=True)