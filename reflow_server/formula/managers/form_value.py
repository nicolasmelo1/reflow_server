from django.db import models

class FormValueFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def values_by_main_formulary_data_id_and_field_id(self, formulary_data_id, field_id):
        """
        This gets all of the values by a single field_id and a main formulary_data_id. This main_formulary_data_id
        is the id of the DynamicForm that has depends_on column as NULL. So not the sections saved but the main 
        formulary data.

        Args:
            formulary_data_id (int): the main_formulary_data_id. These are the DynamicForm instances that have
                                     depends_on_id equal to None
            field_id (int): The field_id to get the data from

        Returns:
            django.db.models.QuerySet(str): Each string of the queryset recieved is the values from the parameters
        """
        return self.get_queryset().filter(
            field_id=field_id, 
            form__depends_on_id=formulary_data_id
        ).values_list('value', flat=True)