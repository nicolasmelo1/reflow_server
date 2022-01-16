from django.db import models

class IntegrationServiceTypeFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def exists_service_name(self, service_name):
        """
        Checks if a given service name actually exists in the database so we can actually authenticate to it.
        
        Args:
            service_name (string): The name of the service to check if exists.

        Returns:
            bool: Return True if the service exists, otherwise it does not exists.
        """
        return self.get_queryset().filter(app_name=service_name).exists()