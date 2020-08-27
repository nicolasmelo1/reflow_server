from django.db import models


class DynamicFormFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def latest_main_dynamic_form_id_by_form_id(self, form_id):
        """
        This retrieves the latest DynamicForm instance id saved of an specific
        formulary. So this doesn't retrieve section ids saved, instead it's MAIN
        formulary ids (DynamicForm intance with depends_on = NULL)

        Args:
            form_id (int): from what Form instance you want to retrieve the latest data.
                           THIS IS NOT THE SECTION FORM instance

        Returns:
            reflow_server.data.models.DynamicForm: The latest DynamicForm instance id saved
                                                   in the database.
        """
        return self.get_queryset().filter(
            form_id=form_id, 
            depends_on__isnull=True
        )\
            .order_by('-updated_at')\
            .values_list('id', flat=True)\
            .first()