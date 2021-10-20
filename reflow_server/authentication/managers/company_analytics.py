from django.db import models


class CompanyAnalyticsAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_company_analytics(self, company_id, number_of_employees, sector):
        """
        Creates a new company analytics used for analytics only and not related at all with the needs of this application.

        Args:
            company_id (int): A Company instance id.
            number_of_employees (str): The number of employees of the company.
            sector (str): The market sector that the company operates.

        Returns:
            reflow_server.analytics.models.CompanyAnalytics: A new or an old and updated CompanyAnalytics instance.
        """
        instance, __ =  self.get_queryset().update_or_create(
            company_id=company_id,
            defaults={
                'number_of_employees': number_of_employees,
                'sector': sector
            }
        )
        return instance