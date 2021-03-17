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
    def bulk_create_and_delete(self, public_access_key, public_access_id, public_form_id, field_ids):
        """
        Gives public access for a list of field_ids, and removes the public access of the field_ids that are not on
        this list. This occurs for a specific `public_form_id`

        Args:
            public_access_key (str): The public_access_key that is a uuid used to represent the user for unauthenticated users
            public_access_id (int): A PublicAccess instance id, this is used so we can create a PublicAccessField
            public_form_id (int): A PublicAccessForm instance id, this is the instance of the public form. To make fields public we need
            to make forms public.
            field_ids (list(int)): List of Field instance ids. Those are the field to consider when saving the formulary.

        Returns:
            bool: Return True indicating that the public fields were created and those that are not on the list were deleted.
        """
        saved_field_ids = self.public_access_fields_by_public_access_key(public_access_key).filter(public_form_id=public_form_id).values_list('field_id', flat=True)
        not_saved_field_ids = [field_id for field_id in field_ids if field_id not in saved_field_ids]
        for field_id in not_saved_field_ids:
            self.get_queryset().create(
                public_access_id=public_access_id,
                public_form_id=public_form_id,
                field_id=field_id
            )
        self.public_access_fields_by_public_access_key(public_access_key).filter(public_form_id=public_form_id).exclude(field_id__in=field_ids).delete()
        return True
    # ------------------------------------------------------------------------------------------
