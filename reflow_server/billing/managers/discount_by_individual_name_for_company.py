from django.db import models


class DiscountByIndividualNameForCompanyBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create(self, individual_charge_value_type_id, value, name, company_id):
        """
        Creates a new discount for each funcionality for the company.

        Args:
            individual_charge_value_type_id (int): A IndividualChargeValueType instance id
            value (float): The value of the discount we want to give to the user 0.90 is 10% discount, 0.85 is 15% discount
                and so on.
            name (str): A unique name for this discount so it can be identifiable
            company_id (int): A Company instance id. For what company you want to give this discount for.

        Returns:
            reflow_server.billing.models.DiscountByIndividualNameForCompany: The newly created instance
        """
        instance = self.get_queryset().create(
            individual_charge_value_type_id=individual_charge_value_type_id,
            value=value,
            name=name,
            company_id=company_id
        )
        return instance