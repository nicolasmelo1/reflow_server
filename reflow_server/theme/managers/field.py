from django.db import models


class FieldThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def update_field_form_field_as_option_id(self, field_id, form_field_as_option_id):
        """
        Updates a single Field instance form_field_as_option_id parameter.
        This is used on `form` field types.

        Args:
            field_id (int): The Field instance id that you want to update
            form_field_as_option_id (int): The Field instance id to use as option. This Field instance is
                                           a Field instance of a section of another formulary
        
        Returns:
            int: number of instances updated, in this case just 1
        """
        return self.get_queryset.filter(id=field_id).update(form_field_as_option_id=form_field_as_option_id)

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