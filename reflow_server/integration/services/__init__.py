from django.utils import timezone

from reflow_server.integration.externals import GoogleExternal
from reflow_server.integration.models import IntegrationAuthentication, IntegrationServiceType

from dateutil.parser import isoparse 
from datetime import timedelta
import json


class IntegrationService: 
    def __init__(self, user_id):
        """
        Class used for interacting with the integrations services, with this we can interact easiliy with the integrations
        services inside of reflow. To interact with the integrations services sometimes what we need are the OAuth2 authentication
        flows. For that we store the access_token and refresh_token in the database.
        """
        from reflow_server.integration.externals import GoogleExternal

        self.google_external = GoogleExternal()
        self.user_id = user_id
    
    def create_user_authentication(self, service_type_name, secret_token=None, access_token=None, refresh_token=None, extra_data=None):
        integration_service_id = IntegrationServiceType.integration_.service_id_by_name(service_type_name)
        if integration_service_id:
            return IntegrationAuthentication.integration_.update_or_create_user_integration_authentication(
                integration_service_id,
                self.user_id,
                secret_token,
                access_token,
                refresh_token,
                extra_data
            )
        else:
            return None
    
    def retrieve_integration_for_company(self, service_type_name, company_id):
        return IntegrationAuthentication.integration_.integration_authentication_by_service_name_and_company_id(
            service_type_name,
            company_id
        )

    def refresh_google_authentication_if_expired(self, integration_authentication):
        """
        Check if the google authentication access_token is expired. If it is refresh the token and retrieve a new token to be used in the
        further request.

        Args:
            integration_authentication (reflow_server.integration.models.IntegrationAuthentication, None): The integration authentication instance.
            if none is recieved we will not do anything and return None directly.
        """
        if integration_authentication != None and integration_authentication.extra_data != None:
            extra_data = json.loads(integration_authentication.extra_data)
            date_generated = isoparse(extra_data['date_generated'])
            # we give more 20 seconds so if for any reason the expired time is not exactly equal the date_generated we will refresh the token
            is_date_generated_and_expiration_invalid = date_generated + timedelta(seconds=extra_data['expires_in'] + 20) < timezone.now()
            exists_client_id = 'client_id' in extra_data
            exists_client_secret = 'client_secret' in extra_data
            exists_refresh_token = integration_authentication.refresh_token != None
            if is_date_generated_and_expiration_invalid and exists_client_id and exists_client_secret and exists_refresh_token:
                google_response = self.google_external.refresh_google_token(
                    extra_data['client_id'], 
                    extra_data['client_secret'], 
                    integration_authentication.refresh_token
                )
                if google_response.status_code == 200:
                    new_data = google_response.json()
                    new_extra_data = json.dumps({
                        'date_generated': timezone.now().isoformat(),
                        'expires_in': new_data['expires_in'],
                        'code': extra_data['code'],
                        'client_id': extra_data['client_id'],
                        'client_secret': extra_data['client_secret'],
                        'scope': extra_data['scope']
                    })
                    return IntegrationAuthentication.integration_.update_or_create_user_integration_authentication(
                        integration_authentication.authentication_type_id,
                        integration_authentication.user_id,
                        integration_authentication.secret_token,
                        new_data['access_token'],
                        integration_authentication.refresh_token,
                        new_extra_data
                    )
            else:
                return integration_authentication

        return None