from django.db import models

class IntegrationAuthenticationFormulaManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def integration_authentication_by_user_id_and_service_name(self, user_id, integration_service_name):
        """
        This will retrieve the authentication data for a given user and a specific integration service name.
        Integration service name is for example 'facebook' or 'google_sheets', 'google_agenda' and others.

        Args:
            user_id (int): The user id to retrieve the authentication data.
            integration_service_name (string): The name of the integration service to retrieve the authentication data.
        
        Returns:
            reflow_server.integration.models.IntegrationAuthentication: The authentication data for the given user and 
            integration service name.
        """
        return self.get_queryset().filter(user_id=user_id, authentication_type__app_name=integration_service_name).first()
