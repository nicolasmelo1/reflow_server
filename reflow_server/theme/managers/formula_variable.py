from django.db import models


class FormulaVariableThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def variable_ids_by_field_id(self, field_id):
        """
        Retrieves all of the formula variable ids by the field_id

        Args:
            field_id (int): The Field instance id to retrieve the variables for

        Returns:
            django.db.models.QuerySet(int): A QuerySet of Field instance ids, which are variables of a formula.
        """
        return self.get_queryset().filter(field_id=field_id).values_list('variable_id', flat=True)