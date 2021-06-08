from django.db import models


class FormulaVariableFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def save_formula_variable(self, field_id, variable_id, order):
        instance, __ = self.get_queryset().update_or_create(
            field_id=field_id,
            variable_id=variable_id,
            order=order
        )
        return instance

    def delete_formula_variables_not_in_variable_ids_by_field_id(self, field_id, variable_ids):
        return self.get_queryset().filter(field_id=field_id).exclude(variable_id__in=variable_ids).delete()