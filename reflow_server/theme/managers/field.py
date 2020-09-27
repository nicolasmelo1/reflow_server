from django.db import models


class FieldThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def fields_by_company_id_and_main_form_ids(self, company_id, main_form_ids):
        """
        Returns a queryset of Field instances from a list of formularies ids (these are not sections)
        and from a specific company.

        Args:
            company_id (int): The Company instance id to filter the fields from
            main_form_ids (list(int)): A list of Form instance ids, those are from MAIN FORMS (so instances with depends_on = None)

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Field): A queryset of field instances
        """
        return self.get_queryset().filter(form__depends_on__group__company_id=company_id, form__depends_on__in=main_form_ids)