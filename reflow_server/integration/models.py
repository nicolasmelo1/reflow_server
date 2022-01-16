from django.db import models

from reflow_server.integration.managers import IntegrationServiceTypeIntegrationManager, \
    IntegrationAuthenticationIntegrationManager
from reflow_server.formula.managers import IntegrationServiceTypeFormulaManager, \
    IntegrationAuthenticationFormulaManager


class IntegrationServiceType(models.Model):
    """
    This model will hold all of the possible services we can connect to. This is used so we can authenticate the user in
    the following server when he is using a formula or when he is using some other service that require authentication elsewhere.
    That's the hole idea for this. If a service that the user cannot authenticate is provided then we do not store this
    information in the database.
    """
    app_name = models.CharField(max_length=500)

    class Meta:
        db_table = 'integration_service_type'

    objects = models.Manager()
    integration_ = IntegrationServiceTypeIntegrationManager()
    formula_ = IntegrationServiceTypeFormulaManager()
    

class IntegrationAuthentication(models.Model):
    """
    This model will hold all of the authentication of the user for integrations. What this means is that this will hold
    the authentication information for the user in a service. With this we can authenticate the user in a given service 
    and interact with it. For example, we can create a new row in the google sheets sheet, we can remove a row in a 
    google sheets sheet and so on.
    """
    authentication_type = models.ForeignKey('integration.IntegrationServiceType', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, null=True)
    secret_token = models.CharField(max_length=500, null=True, blank=True)
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'integration_authentication'

    objects = models.Manager()
    formula_ = IntegrationAuthenticationFormulaManager()
    integration_ = IntegrationAuthenticationIntegrationManager()
    