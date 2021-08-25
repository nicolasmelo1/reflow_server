from django.db import models


class FormValueFilterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def values_of_form_field_type_by_field_id_and_field_type_id(self, field_id, field_type_id):
        return self.get_queryset().annotate(
            value2=models.functions.comparison.Cast('value', output_field=models.IntegerField())
        ).filter(
            field_id=field_id, 
            field_type_id=field_type_id
        ).values_list('value2', flat=True)
    
    def main_form_id_section_id_and_value_by_field_id_and_form_data_ids_or_section_data_ids(self, field_id, form_data_ids_or_section_data_ids):
        return self.get_queryset().filter( 
            models.Q(field_id=field_id, form_id__in=form_data_ids_or_section_data_ids) |
            models.Q(field_id=field_id, form__depends_on_id__in=form_data_ids_or_section_data_ids)
        ).values(
            'form__depends_on_id', 
            'form_id', 
            'value'
        )
    
    def latest_form_value_field_type_by_field_id(self, field_id):
        try:
            return self.get_queryset().filter(field_id=field_id).latest('updated_at')
        except:
            return None