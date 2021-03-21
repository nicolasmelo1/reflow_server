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
