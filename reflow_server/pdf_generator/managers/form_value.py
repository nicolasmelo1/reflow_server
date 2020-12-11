from django.db import models
from django.db.models import Q

class FormValuePDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def form_values_by_field_ids_and_form_data_id_and_forms_connected_to(self, field_ids, form_data_id, forms_connected_to=[]):
        """
        This retrieves the FormValue instances that match 3 possible conditions:
        1º - When the connected form depends_on a DynamicForm instance id of the FormValue is one 
             and the id of the field is in a list of field ids
        2º - When the connected form is of a DynamicForm instance id and and 
             the id of the field is in a list of field ids
        3º - When the form_field_as_option of the field is from a list of ids in forms_connected_to
             and the form it is connected to depends on the `form_data_id`.

        Args:
            field_ids (list(int)): A list of reflow_server.formulary.models.Field instance ids
            form_data_id (int): A reflow_server.data.models.DynamicForm intance id, this instance could have
                                either the depends_on as None or not.
            forms_connected_to (list(int), optional): A list of reflow_server.formulary.models.Form instances. Defaults to [].

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A Queryset of FormValue intances that 
                                                                            match any of the conditions above
        """
        return self.get_queryset().filter(
            Q(form__depends_on_id=form_data_id, field_id__in=field_ids) | 
            Q(form_id=form_data_id, field_id__in=field_ids) | 
            Q(field__form_field_as_option__form__depends_on_id__in=forms_connected_to, form__depends_on_id=form_data_id)
        )
    