from django.db import models

class CompanyAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def company_by_id(self, company_id):
        """
        Retrieves a given company instance by the company_id.

        Args:
            company_id (int): The id of the company we want to retrieve.

        Returns:
            reflow_server.authentication.models.Company: The company instance to retrieve by the given company_id.
        """
        return self.get_queryset().filter(id=company_id).first()