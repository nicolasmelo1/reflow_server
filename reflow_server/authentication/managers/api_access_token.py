from django.db import models

import uuid


class APIAccessTokenAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create(self, company_id, user_id):
        """
        Actually just create a new access token if it doesn't exist.

        Args:
            company_id (int): The Company instance id.
            user_id (int): The User instance id.
        
        Returns:
            reflow_server.authentication.models.APIAccessToken: The created APIAccessToken instance.
        """
        instance = self.get_queryset().create(
            user_id=user_id, 
            company_id=company_id, 
            access_token=str(uuid.uuid4())
        )
        return instance

    def delete(self, company_id, user_id):
        return self.get_queryset().filter(user_id=user_id, company_id=company_id).delete()

    def user_id_by_secret_access_token_and_company_id(self, secret_access_token, company_id):
        """
        Checks if the secret access token being used exists for the company and retrieves the user_id for it.

        Args:
            secret_access_token (str): The secret_access_token to identify what user is trying to access the api.
            company_id (int): The Company instance id.

        Returns:
            (int|None): A User instance id or None if it doesn't exists
        """
        return self.get_queryset().filter(access_token=secret_access_token, company_id=company_id).values_list('user_id', flat=True).first()

    def exists_by_user_id_and_company_id(self, user_id, company_id):
        return self.get_queryset().filter(user_id=user_id, company_id=company_id).exists()