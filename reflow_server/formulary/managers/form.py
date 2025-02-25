from django.db import models


class FormFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def first_form_name_from_group_id(self, group_id):
        return self.get_queryset().filter(group_id=group_id).order_by('order').values_list('form_name', flat=True).first()

    def form_sections_by_section_ids_company_ids_and_main_form_id(self, section_ids, company_id, main_form_id):
        """
        Returns a queryset of Form instances that are sections (so have depends_on as NOT NULL) by it's company_id, and the main_form_id

        Args:
            section_ids (list(int)): A list of Form instance ids where each Form instance have depends_on as NOT NULL
            company_id (int): A Company instance id
            main_form_id (int): A form instance id where the instance have depends_on AS NULL

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Form): A queryset of Form instances, where each form instance is actually a section.
        """
        return self.get_queryset().filter(id__in=section_ids, depends_on__group__company_id=company_id, depends_on_id=main_form_id)
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
    # ------------------------------------------------------------------------------------------
    def count_main_forms_by_company_id(self, company_id):
        """
        Counts all of the formularies (not the sections) of a given company_id.

        Args:
            company_id (int): The id of a Company instance.

        Returns:
            int: The number of main forms of a given company_id.
        """
        return self.get_queryset().filter(group__company_id=company_id, depends_on_id__isnull=True).count()