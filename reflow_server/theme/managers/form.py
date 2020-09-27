from django.db import models


class FormThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def main_forms_by_company_id_and_form_ids(self, company_id, form_ids):
        """
        Returns the main forms of a list of formulary ids (those are the main form ids, not the section ones) and
        from a company_id.

        Args:
            company_id (int): The Company instance id to filter the forms from
            form_ids (list(int)): A list of Form instance ids, those are from MAIN FORMS (so instances with depends_on = None)

        Returns:
            django.db.QuerySet(reflow_server.formulary.models.Form): A queryset of main forms, all of the Form instances here have 
            depends_on as None
        """
        return self.get_queryset().filter(id__in=form_ids, group__company_id=company_id, depends_on__isnull=True)

    def section_forms_by_company_id_and_main_form_ids(self, company_id, main_form_ids):
        """
        Returns the section forms based of a list of formulary ids (those are the main form ids, not the section ones) and
        from a company_id.

        Args:
            company_id (int): The Company instance id to filter the forms from
            form_ids (list(int)): A list of Form instance ids, those are from MAIN FORMS (so instances with depends_on = None)

        Returns:
            django.db.QuerySet(reflow_server.formulary.models.Form): A queryset of section forms, all of the Form instances here have 
            depends_on as NOT None
        """
        return self.get_queryset().filter(depends_on__in=main_form_ids, depends_on__group__company_id=company_id)