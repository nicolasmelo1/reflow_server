from django.db import models


class PublicAccessFieldFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
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
        return self.get_queryset().filter(public_access__public_key=public_access_key).values_list('field_id', flat=True)
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
        return self.get_queryset().filter(public_access__public_key=public_access_key).values_list('field__form_id', flat=True).distinct()
    # ------------------------------------------------------------------------------------------
