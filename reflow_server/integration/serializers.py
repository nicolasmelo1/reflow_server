from rest_framework import serializers

from reflow_server.integration.models import IntegrationAuthentication
from reflow_server.integration.services import IntegrationService

class IntegrationAuthenticationSerializer(serializers.ModelSerializer):
    def save(self, service_name, user_id):
        integration_service = IntegrationService(user_id)
        return integration_service.create_user_authentication(
            service_name, 
            self.validated_data.get('secret_token', None),
            self.validated_data.get('access_token', None),
            self.validated_data.get('refresh_token', None),
            self.validated_data.get('extra_data', None)
        )

    class Meta:
        model = IntegrationAuthentication
        fields = ['secret_token', 'access_token', 'refresh_token', 'extra_data']

