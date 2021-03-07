from django.db import models


class PublicAccessFormFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    # ------------------------------------------------------------------------------------------
    def exists_public_access_form_by_public_access_key_and_main_form_name(self, public_access_key, main_form_name):
        return self.get_queryset().filter(public_access__public_key=public_access_key, form__form_name=main_form_name).exists()
