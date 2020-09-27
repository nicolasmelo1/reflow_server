from django.db import models


class FieldOptionsThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def field_options_by_field_id(self, field_id):
        """
        Gets a queryset of FieldOption instances from a single field_id

        Args:
            field_id (int): The field instance id you want to filter the options on

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.FieldOption): returns a queryset
            of FieldOption instances.
        """
        return self.get_queryset().filter(field_id=field_id)

