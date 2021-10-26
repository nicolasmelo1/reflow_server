from django.db import models


class APIAccessTokenAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

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