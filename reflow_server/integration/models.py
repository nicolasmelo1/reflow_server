from django.db import models

# Create your models here.
class IntegrationAuthenticationType(models.Model):
    app_name = models.CharField(max_length=500)

    class Meta:
        db_table = 'integration_authentication_type'


class IntegrationAuthentication(models.Model):
    authentication_type = models.ForeignKey('integration.IntegrationAuthenticationType', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, null=True)
    secret_token = models.CharField(max_length=500, null=True, blank=True)
    access_token = models.CharField(max_length=500, null=True, blank=True)
    refresh_token = models.CharField(max_length=500, null=True, blank=True)
    extra_data = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'integration_authentication'