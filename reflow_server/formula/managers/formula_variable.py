from django.db import models

class FormulaVariableFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def variable_ids_by_field_id(self, field_id):
        return self.get_queryset().filter(field_id=field_id).values_list('variable_id', flat=True)