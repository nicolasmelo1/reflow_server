from django.db import models


class CompanyBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def company_by_company_id(self, company_id):
        """
        Retrives a single Company instance object by the company_id.

        Args:
            company_id (int): The id of the Company instance you want to retrieve

        Returns:
            reflow_server.authentication.models.Company: The company instance that matches the id given
        """
        return self.get_queryset().filter(id=company_id).first()

    def update_is_active_by_company_id(self, company_id, is_active):
        """
        Updates the company status (if is active or not). If the company is not active then the user cannot
        use the platform anymore, otherwise he can use normally.

        Args:
            company_id (int): The id of the Company instance you want to update
            is_active (bool): Boolean signaling if the company is active or not.

        Returns:
            reflow_server.authentication.models.Company: The updated company instance.
        """
        instance = self.company_by_company_id(company_id)
        instance.is_active = is_active
        instance.save()
        return instance