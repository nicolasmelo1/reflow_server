from django.db import models


class IntegrationAuthenticationIntegrationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def update_or_create_user_integration_authentication(self, integration_type_id, user_id, secret_token=None, access_token=None, refresh_token=None, extra_data=None):
        """
        This will update or create a new authentication for the user, this way we can authenticate him in a service, for example, 
        google sheets. This is used so we can authenticate him in stuff like formulas or future no-code automations.

        Args:
            integration_type_id (int): The id of the integration type. The services the user can authenticate are defined in
                the integration_service_type table, so see there first for what the id is for the given service name.
            user_id (int): The id of the user we are authenticating to.
            secret_token (str | None): The secret token for the authentication. Only needed when this is retrieved from the app.
            access_token (str | None): The access token for the authentication. Only needed when this is retrieved from the app.
            refresh_token (str | None): The refresh token for the authentication. Only needed when this is retrieved from the app.
            extra_data (str | None): This is a JSON string that can be used to store extra data for the authentication.

        Returns:
            reflow_server.integration.models.IntegrationAuthentication: The authentication object so we use it the next time we want
            to retrieve the authentication for this user.
        """
        instance, __ = self.get_queryset().update_or_create(
            authentication_type_id=integration_type_id,
            user_id=user_id,
            defaults={
                'secret_token': secret_token,
                'access_token': access_token,
                'refresh_token': refresh_token,
                'extra_data': extra_data
            }
        )
        return instance

    def integration_authentication_by_service_name_and_company_id(self, service_name, company_id):
        """
        Retrieves a single authentication type based on a service name and a given company_id.

        Args:
            service_name (str): The name of the service we are authenticating to.
            company_id (int): The id of the company we are authenticating to.
        
        Returns:
            reflow_server.integration.models.IntegrationAuthentication: The authentication object so we 
            use it the next time we want
        """
        return self.get_queryset().filter(authentication_type__app_name=service_name, user__company_id=company_id).first()