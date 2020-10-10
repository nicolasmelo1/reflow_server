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
            django.db.models.QuerySet(reflow_server.formulary.models.Form): A queryset of main forms, all of the Form instances here have 
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
            django.db.models.QuerySet(reflow_server.formulary.models.Form): A queryset of section forms, all of the Form instances here have 
            depends_on as NOT None
        """
        return self.get_queryset().filter(depends_on__in=main_form_ids, depends_on__group__company_id=company_id)

    def update_section_conditional_on_field(self, form_section_id, field_id):
        """
        Updates the condiditional_on_field attribute of a single Form section instance based on its id 

        Args:
            form_section_id (int): The id of the Form you want to update. Usually, this id is of an instance
                                         that has Form depends_on=None
            field_id (int): The id of the field you want to use as conditional for this section

        Returns:
            int: Returns the number of affected rows, usually 1: https://docs.djangoproject.com/en/dev/ref/models/querysets/#update
        """
        return self.get_queryset().filter(id=form_section_id, depends_on__isnull=False).update(conditional_on_field_id=field_id)
    
    def main_form_name_by_company_id_last_created(self, company_id):
        """
        Returns the last created main form of a single company_id.

        Args:
            company_id (int): The Company instance id to filter the forms from

        Returns:
            str: The last created main formulary `form_name`
        """
        return self.get_queryset().filter(depends_on__isnull=True, group__company_id=company_id).order_by('-created_at').values_list('form_name', flat=True).first()