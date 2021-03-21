from django.db import models


class PublicAccessAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def update_or_create(self, user_id, company_id):
        """
        Updates or creates a new PublicAccess, a public access instance is just a uuid that is a key
        that is used to represent the user. When another unauthenticated user access anything "publicly available" with this key
        then our system understands the this unauthenticated user is actually the user responsible for this key.

        Args:
            user_id (int): A UserExtended instance id, this is the user_id the public_access_key wil represent
            company_id (int): A Company instance id, the public access key is unique for each company.

        Returns:
            reflow_server.authentication.models.PublicAccess: The created or updated PublicAccess instance
        """
        instance, __ = self.get_queryset().update_or_create(
            user_id=user_id,
            company_id=company_id
        )
        return instance