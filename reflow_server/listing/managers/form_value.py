from django.db import models


class FormValueListingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def form_values_by_main_form_ids_company_id(self, main_form_ids, company_id):
        """
        Gets the form_values from a list of main_form_ids (those are not section ids) and from a company_id

        Args:
            main_form_ids (list(int)): a list of DynamicForm instance ids where depends_on IS NULL.
            company_id (int): a Company instance id.

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): Returns a queryset of FormValue instances from the parameters
            recieved
        """
        return self.get_queryset().filter(form__depends_on_id__in=main_form_ids, company_id=company_id)

    