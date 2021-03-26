from django.db import models


class DefaultValueFieldAttachmentsFormularyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def update_or_create(self, file_name, file_size, file_url, default_value_field_attachment_id=None):
        """
        Updates or creates a singe DefaultValueFieldAttachments instance.

        Args:
            file_name (str): The name of the file
            file_size (int): The size of the file in bytes
            file_url (str): The url of where the file is located
            default_value_field_attachment_id (int, optional): If you are updating an instance
            this is the instance id you are updating. Defaults to None.

        Returns:
            reflow_server.formulary.models.DefaultValueFielAttachments: The created or updated instance.
        """
        instance, __ = self.get_queryset().update_or_create(
            id=default_value_field_attachment_id,
            defaults={
                'file': file_name,
                'file_size': file_size,
                'file_url': file_url
            }
        )
        return instance
