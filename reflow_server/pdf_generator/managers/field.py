from django.db import models


class FieldPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def fields_by_main_form_id(self, main_form_id):
        """
        Retrieves all of the fields by the main_form_id. The main_form_id is the id of the formulary.

        Args:
            main_form_id (int): An reflow_server.formulary.models.Form instance id where depends_on is None

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Field): A queryset of fields instances
        """
        return self.get_queryset().filter(form__depends_on_id=main_form_id)

    def form_fields_by_main_form_id_and_company_id(self, main_form_id, company_id):
        """
        Retrieves only fields of type 'form' by the main_form_id and the company_id. As explained above, the
        main_form_id is an formulary instance id.

        Args:
            main_form_id (int): An reflow_server.formulary.models.Form instance id where depends_on is None
            company_id (int): An reflow_server.authentication.models.Company instance id

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Field): A queryset of 'form' type field instances
        """
        return self.get_queryset().filter(form__depends_on__group__company_id=company_id, form__depends_on_id=main_form_id, type__type='form')