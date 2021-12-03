from django.db import models


class ProfileTypeAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def coordinator_profyle_type(self):
        return self.get_queryset().filter(name='coordinator').first()