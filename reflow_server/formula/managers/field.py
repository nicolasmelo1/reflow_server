from django.db import models


class FieldFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def date_format_id_number_format_id_and_form_field_as_option_id_field_type_by_field_id(self, field_id):
        """
        Returns the `date_configuration_date_format_type_id`, the `number_configuration_number_format_type_id`, the
        `form_field_as_option_id` and the `type` of a field_id

        Args:
            field_id (int): A Field instance id.

        Returns:
            dict({
                'form_field_as_option_id': int
                'number_configuration_number_format_type_id': int
                'date_configuration_date_format_type_id': int
                'type__type': str
            }): A dict with the following keys of a single field_id
        """
        return self.get_queryset().filter(id=field_id).values(
            'form_field_as_option_id', 
            'number_configuration_number_format_type_id',
            'date_configuration_date_format_type_id',
            'type__type'
        ).first()