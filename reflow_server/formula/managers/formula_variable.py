from django.db import models


class FormulaVariableFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def variable_ids_by_field_id(self, field_id):
        """
        Retrieves a queryset of all of the variable_ids of a field_id.
        Just remember: variable_ids are field_ids. 

        Args:
            field_id (int): A Field instance id. This field_id is the `formula` field type, with the 
                            formula_configuration defined

        Returns:
            django.db.models.QuerySet(int): A queryset of variable_ids
        """
        return self.get_queryset().filter(field_id=field_id).values_list('variable_id', flat=True)