from django.db import models

class IntegrationServiceTypeIntegrationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def service_id_by_name(self, service_type_name):
        """
        This will retrieve the id of the service based on the name of the service.

        Args:
            service_type_name (str): The name of the service.

        Returns:
            int: The id of the service.
        """
        return self.get_queryset().filter(app_name=service_type_name).values_list('id', flat=True).first()