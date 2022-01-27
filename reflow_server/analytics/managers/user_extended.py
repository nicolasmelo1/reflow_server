from django.db import models
from django.utils import timezone


class UserExtendedAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def user_by_id(self, user_id):
        """
        Retrieves a user instance by the given user_id.

        Args:
            user_id (int): The id of the user we want to retrieve.

        Returns:
            reflow_server.authentication.models.UserExtended: The user instance to retrieve by the given user_id.
        """
        return self.get_queryset().filter(id=user_id).first()

    def has_user_joined_reflow_from_at_least_30_days(self, user_id):
        """
        Checks if a given user_id has joined reflow for more than 30 days. If it has than we can safely send surveys for him

        Args:
            user_id (int): The id of the user we want to check if has created a reflow account for more than 30 days.

        Returns:
            bool: True if the user has joined reflow for more than 30 days, False otherwise.
        """
        date_to_check = timezone.now() - timezone.timedelta(days=30)
        return self.get_queryset().filter(id=user_id, date_joined__lte=date_to_check).exists()