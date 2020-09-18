from django.db import models


class CompanyAuthenticationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_company(self, company_name, company_endpoint, partner, shared_by=None):
        """
        Creates a new company, this is usually created only on onboarding.

        Args:
            company_name (str): This is the name of the company, every company 
            should have a name. Sometimes the user don't want to name a company, so 
            we name it automatically for them
            company_endpoint (str): The endpoint of the company is used when the user
            wants to share something for someone. It's usually a url friendly string. 
            partner (str): We have partners programs, with this we can know how many users
            came from a partner and how much we should give them in return.
            shared_by (reflow_server.authentication.models.Company, optional): If the
            user has come from a link from any company we save this here to know that the
            company came from another one. This way we can give them discounts. Defaults to None.

        Returns:
            reflow_server.authentication.models.Company: The created company instance
        """
        instance = self.get_queryset().create(
            name=company_name,
            is_active=True,
            endpoint=company_endpoint,
            shared_by=shared_by,
            partner=partner
        )
        return instance

    def company_by_company_id(self, company_id):
        """
        Retrives a single Company instance object by the company_id.

        Args:
            company_id (int): The id of the Company instance you want to retrieve

        Returns:
            reflow_server.authentication.models.Company: The company instance that matches the id given
        """
        return self.get_queryset().filter(id=company_id).first()
    
    def company_by_endpoint(self, endpoint):
        """
        Retrives a single Company instance object by the company endpoint. If you didn't knew, each 
        company endpoint is unique for each company.

        Args:
            company_id (int): The id of the Company instance you want to retrieve

        Returns:
            reflow_server.authentication.models.Company: The company instance that matches the id given
        """
        return self.get_queryset().filter(endpoint=endpoint).first()