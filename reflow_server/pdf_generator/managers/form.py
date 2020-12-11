from django.db import models


class FormPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def formulary_by_company_id_and_form_name(self, company_id, form_name):
        """
        Returns a Form instance by it's form_name and the company it is bounded to

        Args:
            company_id (int): An reflow_server.authentication.models.Company instance id
            form_name (str): A formulay name, it works as an id for each formulary of the company.
                             this is usually what we use on the url.

        Returns:
            reflow_server.formulary.models.Form: returns a single formulary instance that matches the condition.
        """
        return self.get_queryset().filter(group__company_id=company_id, form_name=form_name).first()