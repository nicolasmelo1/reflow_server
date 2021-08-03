from django.db import models


class FormListingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def form_id_by_company_id_and_form_name(self, company_id, form_name):
        """
        Retrieves the form_id by the name of the formulary.

        Args:
            company_id (str): The Company instance id.
            form_name (str): The formulary name
        
        Returns:
            (None, int): Returns None if no formulary is found or an int if it does
        """
        return self.get_queryset().filter(group__company_id=company_id, form_name=form_name).values_list('id', flat=True).first()