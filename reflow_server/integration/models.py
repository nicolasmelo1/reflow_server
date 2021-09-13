from django.db import models

# Create your models here.
class IntegrationAuthentication(models.Model):
    app_name = models.CharField(max_length=500)

    class Meta:
        db_table = 'integration_authentication'