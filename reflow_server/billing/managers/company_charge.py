from django.db import models


class CompanyChargeBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def create_company_charge(self, company, total_value, attempt_count):
        """
        Creates a new company charge for a specific company. Remember that Company Charges are the charges
        that a company has already paid.
        Usually this is something that we recieve from the payment gateway.

        Args:
            company (reflow_server.authentication.models.Company): The Company instance that has paid a invoice
            total_value (float): How much was the invoice that he paid.
            attempt_count (int): How many tries until he paid.
        
        Returns:
            reflow_server.billing.models.CompanyCharge: The instance of the created CompanyCharge in our database.
        """
        instance = self.create(
            company=company,
            total_value=total_value,
            attempt_count=attempt_count
        )

        return instance

    def exists_company_charge_created_between_dates_by_company(self, company_id, date_start, date_end):
        """
        Check if a company charge of a specific company_id was created between two dates.

        Args:
            company_id (int): The id of a Company instance.
            date_start (datetime.datetime): The start date of the date range
            date_end (datetime.datetime): The end date of the date range

        Returns:
            bool: Returns True or False if the CompanyCharge exists for this company between the end and the start dates.
        """
        return self.get_queryset().filter(
            company_id=company_id, created_at__gte=date_start, created_at__lte=date_end
        ).exists()