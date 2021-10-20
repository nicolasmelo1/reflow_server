from django.db import models


class FormDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    # ------------------------------------------------------------------------------------------
    def sections_enabled_by_main_form_name_and_company_id(self, main_form_name, company_id):
        return self.get_queryset().filter(
            depends_on__form_name= main_form_name, 
            depends_on__group__company_id=company_id, 
            enabled=True
        )
    # ------------------------------------------------------------------------------------------
    def form_by_form_name_of_company_id(self, main_form_name, company_id):
        return self.get_queryset().filter(form_name=main_form_name, enabled=True, group__enabled=True, group__company_id=company_id).first()
    # ------------------------------------------------------------------------------------------
    def form_name_by_form_id_and_company_id(self, form_id, company_id):
        """
        Returns a the form_name of a MAIN FORM (Not a section) by it's form_id and the company_id.

        Args:
            form_id (int): The id of a Form instance.
            company_id (int): The id of a Company instance.

        Returns:
            (None, str): Returns the name of the formulary (Remember that the name is similar to the ID of the formulary, it's NOT the label_name)
        """
        return self.get_queryset().filter(id=form_id, group__company_id=company_id).values_list('form_name', flat=True).first()