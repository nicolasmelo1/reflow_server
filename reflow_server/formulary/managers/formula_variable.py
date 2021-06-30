from django.db import models


class FormulaVariableFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def save_formula_variable(self, field_id, variable_id, uuid, order):
        instance, __ = self.get_queryset().update_or_create(
            uuid=uuid,
            defaults={
                'field_id': field_id,
                'variable_id': variable_id,
                'order': order
            }
        )
        return instance

    def delete_formula_variables_not_in_variable_ids_by_uuids(self, field_id, uuids):
        return self.get_queryset().filter(field_id=field_id).exclude(uuid__in=uuids).delete()