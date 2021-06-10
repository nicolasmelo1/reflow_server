from django.db import models

class FormulaVariableFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def formula_variables_by_field_id(self, field_id):
        return self.get_queryset().filter(field_id=field_id)