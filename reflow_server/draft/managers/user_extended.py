from django.db import models


class UserExtendedDraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def users_active_by_company_id(self, company_id):
        """
        Retrieves a queryset of ACTIVE UserExtended instances

        Args:
            company_id (int): An Company instance id that the users must be from.

        Returns:
            django.db.models.QuerySet(reflow_server.authentication.models.UserExtended): An queryset of UserExtended instances
                                                                                         from the company selected
        """
        return self.get_queryset().filter(company_id=company_id, is_active=True)