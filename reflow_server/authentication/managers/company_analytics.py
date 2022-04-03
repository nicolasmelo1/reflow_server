from django.db import models


class CompanyAnalyticsAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_company_analytics(self, company_id):
        """
        Creates a new company analytics used for analytics only and not related at all with the needs of this application.

        Args:
            company_id (int): A Company instance id.

        Returns:
            reflow_server.analytics.models.CompanyAnalytics: A new or an old and updated CompanyAnalytics instance.
        """
        instance, __ =  self.get_queryset().update_or_create(
            company_id=company_id
        )
        return instance