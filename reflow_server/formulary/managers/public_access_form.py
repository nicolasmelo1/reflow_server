from django.db import models


class PublicAccessFormFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    # ------------------------------------------------------------------------------------------
    def exists_public_access_form_by_public_access_key_and_main_form_name(self, public_access_key, main_form_name):
        return self.get_queryset().filter(public_access__public_key=public_access_key, form__form_name=main_form_name).exists()
    # ------------------------------------------------------------------------------------------
    def update_or_create(self, public_access_id, form_id):
        instance, __ = self.get_queryset().update_or_create(
            public_access_id=public_access_id, 
            form_id=form_id
        )
        return instance
    # ------------------------------------------------------------------------------------------
    def delete_by_public_access_key_and_main_form_id(self, public_access_key, main_form_id):
        return self.get_queryset().filter(public_access__public_key=public_access_key, form_id=main_form_id).delete()
