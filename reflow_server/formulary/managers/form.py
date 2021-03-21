from django.db import models


class FormFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

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