from django.db import models

class DynamicFormPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def main_formulary_data_id_by_section_data_id(self, section_data_id):
        """
        Retrieves the main_form_data_id based on a section data instance id.
        main_form_data_id is a DynamicForm instance id where depends_on IS NOT None

        Args:
            section_data_id (): A DynamicForm instance id where depends_on is None

        Returns:
            int: a DynamicForm instance id where depends_on IS NOT None
        """
        return self.get_queryset().filter(id=section_data_id).values_list('depends_on_id', flat=True).first()