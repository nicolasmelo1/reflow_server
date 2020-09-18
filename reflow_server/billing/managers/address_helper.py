from django.db import models


class AddressHelperBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_all(self):
        """
        Retrives a queryset of all of the Address Helper instances

        Returns:
            django.db.models.QuerySet(reflow_server.models.authentication.AddressHelper): Queryset containing all of the
            AddressHelper instances
        """
        return self.get_queryset().all()