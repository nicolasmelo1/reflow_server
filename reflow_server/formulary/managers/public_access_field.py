from django.db import models


class PublicAccessFieldFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    # ------------------------------------------------------------------------------------------
    def public_access_fields_by_public_access_key(self, public_access_key):
        return self.get_queryset().filter(public_access__public_key=public_access_key)
    # ------------------------------------------------------------------------------------------
    def exists_field_id_by_public_access_key_and_form_name(self, public_access_key, field_id, main_form_name):
        return self.public_access_fields_by_public_access_key(public_access_key).filter(public_form__form__form_name=main_form_name, field_id=field_id).exists()
    # ------------------------------------------------------------------------------------------
    def field_ids_by_public_access_key(self, public_access_key):
        """
        Retrieves all of the field ids of a certain public_access_key

        Args:
            public_access_key (str): The public acess key, this is a simple uuid string, defined in PublicAccess model. Each public_access_key
            is bounded for a single user.

        Returns:
            django.db.models.QuerySet(int): A queryset of Field instance ids.
        """
        return self.public_access_fields_by_public_access_key(public_access_key).values_list('field_id', flat=True)
    # ------------------------------------------------------------------------------------------
    def section_ids_by_public_access_key(self, public_access_key):
        """
        Retrieves all of the form section ids of a certain public_access_key

        Args:
            public_access_key (str): The public acess key, this is a simple uuid string, defined in PublicAccess model. Each public_access_key
            is bounded for a single user.

        Returns:
            django.db.models.QuerySet(int): A queryset of Form section ids. Those Form instances have depends_on as NOT NONE
        """
        return self.public_access_fields_by_public_access_key(public_access_key).values_list('field__form_id', flat=True).distinct()
    # ------------------------------------------------------------------------------------------
