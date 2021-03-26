from django.db import models


class DefaultFieldValueFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def default_field_values_by_field_id_excluding_default_field_value_ids(self, field_id, default_field_value_ids):
        """
        Retrieves a queryset of DefaultFieldValue instances by a specific field_id and excluding a list of default_field_value_ids

        Args:
            field_id (int): A Field instance id
            default_field_value_ids (list(int)): List of DefaultFieldValue instance ids
        
        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.DefaultFieldValue): A queryset of DefaultFieldValue that matches the criteria.
        """
        return self.get_queryset().filter(field_id=field_id).exclude(id__in=default_field_value_ids)

    def delete_default_field_values_by_field_id_excluding_default_field_value_ids(self, field_id, default_field_value_ids):
        """
        Delete DefaultFieldValue instances by a field_id and excluding a list of default_field_value_ids

        Args:
            field_id (int): A Field instance id
            default_field_value_ids (list(int)): List of DefaultFieldValue instance ids

        Returns:
            int: The number of deleted instances
        """
        return self.default_field_values_by_field_id_excluding_default_field_value_ids(field_id, default_field_value_ids).delete()

    def default_value_field_by_default_value_field_attachment_file_name_field_id_and_company_id(self, file_name, field_id, company_id):
        """
        Returns a default DefaultFieldValue instance by a particular field_id from a specific company, from a specific main form, and
        with an specific attachment file_name, we use this to retrieve the file for the field_value

        Args:
            file_name (str): The name of the file you want to retrieve
            field_id (int): A Field instance id
            company_id (int): A Company instance id

        Returns:
            reflow_server.formulary.models.DefaultFieldValue: Returns the DefaultFieldValue instance that matches the criteria
        """
        return self.get_queryset().filter(field_id=field_id, field__form__depends_on__group__company_id=company_id, default_attachment__file=file_name).first()

    def update_or_create(self, field_id, value, default_field_value_id=None):
        """
        Updates or creates a new DefaultFieldValue. Those values are the values that will automatically be inserted
        whenever a new formulary is created.

        Args:
            field_id (int): A field instance id
            value (str): The default value to use for this field
            default_field_value_id (int, optional): If you are updating this is the DefaultFieldValue instance id of the instance
                                                    you are updating. Defaults to None.

        Returns:
            reflow_server.formulary.models.DefaultFieldValue: The instance created or updated
        """
        instance, __ = self.get_queryset().update_or_create(
            id=default_field_value_id,
            defaults={
                'field_id': field_id,
                'value': value
            }
        )
        return instance