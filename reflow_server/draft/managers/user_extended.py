from django.db import models


class UserExtendedDraftManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def user_ids_active_by_company_id(self, company_id):
        """
        Retrieves a queryset of ACTIVE UserExtended instances

        Args:
            company_id (int): An Company instance id that the users must be from.

        Returns:
            django.db.models.QuerySet(int): An queryset of UserExtended instances ids from the company selected
                                            that are active
        """
        return self.get_queryset().filter(company_id=company_id, is_active=True).values_list('id', flat=True)