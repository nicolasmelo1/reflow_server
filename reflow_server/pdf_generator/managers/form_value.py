from django.db import models
from django.db.models import Q

class FormValuePDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def form_values_by_field_ids_and_form_data_id_and_forms_connected_to(self, field_ids, form_data_id, forms_connected_to=[]):
        return self.get_queryset().filter(
            Q(form__depends_on_id=form_data_id, field_id__in=field_ids) | 
            Q(form_id=form_data_id, field_id__in=field_ids) | 
            Q(field__form_field_as_option__form__depends_on_id__in=forms_connected_to, form__depends_on_id=form_data_id)
        )
    