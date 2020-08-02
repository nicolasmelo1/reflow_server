from django.db import transaction

from reflow_server.authentication.models import Company
from reflow_server.billing.services.charge import ChargeService
from reflow_server.billing.services.payment import PaymentService
from reflow_server.billing.services.vindi import VindiService

    
class BillingService:
    def __init__(self, company_id):
        """
        Service for change company charges without much difficulty inside the code. This is also responsible
        for creating a simple interface with billing without the need to import other billing services like 'ChargeService' or 'PaymentService' 
        directly.

        Args:
            company_id (int): Gets the company info from the database so we can make changes to it
        """
        self.company = Company.objects.filter(id=company_id).first()
        self.charge_service = ChargeService(self.company)
        self.payment_service = PaymentService(self.company)
    
    def remove_credit_card(self):
        return VindiService(self.company.id).delete_payment_profile()

    def remove_user(self, user_id, push_updates=True):
        """
        Removes a user from the billing.

        Args:
            user_id (int): the id of the user to remove
            push_updates (bool, optional): Set to False if you don't want to push the updates to our Payment Gateway. 
                                           Defaults to True.

        Returns:
            bool: True or False wheather the removal of the user was successful or not.
        """
        for charge_name in ['per_user', 'per_chart_company', 'per_chart_user']:
            self.charge_service.remove(charge_name, user_id, push_updates)
        return True

    @transaction.atomic
    def create_user(self, user_id, push_updates=True):
        """
        Used for when creating a new user only, when updating you should use `.update()` method directly.
        It just loops for each 'charge_value_names' passing only the name as parameter, this way we always force to use the defauld value.

        Args:
            push_updates (bool, optional): Set to False if you don't want to push the updates to our Payment Gateway. Defaults to True.

        Returns:
            list(reflow_server.billing.models.CurrentCompanyCharge): This data is a list of the instances of the newly created CurrentCompanyCharge.
                                                                     each item on the list represents each row inserted on the database.
        """
        charge_value_names = ['per_user', 'per_chart_company', 'per_chart_user']

        return self.charge_service.create(charge_value_names, user_id=user_id, push_updates=push_updates)

    @transaction.atomic
    def create_company(self, push_updates=True):
        """
        Used for when creating a new company only, when updating you should use `.update()` method directly.
        It just loops for each 'charge_value_names' passing only the name as parameter, this way we always force to use the defauld value.

        Args:
            push_updates (bool, optional): Set to False if you don't want to push the updates to our Payment Gateway. Defaults to True.

        Returns:
            list(reflow_server.billing.models.CurrentCompanyCharge): This data is a list of the instances of the newly created CurrentCompanyCharge.
                                                                     each item on the list represents each row inserted on the database.
        """
        charge_value_names = ['per_gb']

        return self.charge_service.create(charge_value_names, push_updates=push_updates)

    @classmethod
    @transaction.atomic
    def update_billing(cls, company_id, payment_method_type_id, invoice_date_type_id, emails, 
                       current_company_charges, cnpj, zip_code, street, state, 
                       number, neighborhood, country, city, additional_details=None, gateway_token=None):
        """
        Updates billing, so this is a factory method that automatically updates the payment data and also the charge data and pushes it
        to the payment gateway.

        Args:
            company_id (int): The id of the company to update
            payment_method_type_id (int): the reflow_server.billing.models.PaymentMethodType id to use on this particular company, 
                                          is it credit_card or invoice?
            invoice_date_type_id (int): the id of a single reflow_server.billing.models.InvoiceDateType model, in other words, when the
                                        company will be billed.
            emails (list(str)): The list of emails to be used to send the invoice to
            current_company_charges (list(reflow_server.billing.services.data.CompanyChargeData)): Notice that this is a list of a specific object
                                                                                                   so if you are trying to use this method from a serializer
                                                                                                   you need to convert the serializer first.
            cnpj (str): The CNPJ of the company, just numbers as string
            zip_code (str): The zip_code of the company address, just numbers as string
            street (str): The street of where the company is located. Just validate if the city is defined in reflow_server.authentication.models.AddressHelper
                          table.
            state (str): The state of the city where the company is located. Vindi requires us that we follow ISO 3166-2, this should be defined already 
                            in reflow_server.authentication.models.AdressHelper model so you don't need to worry
            number (int): The number of the house or of the building where this company is located. This is from the address of the company
            neighborhood (str): The neighborhood of where the street where this company is located.
            country (str): The country where this company is located, as state, is MUST follow ISO 3166-2, luckly, it is already defined in
                           reflow_server.authentication.models.AddressHelper.
            city (str): Thye city where this company is located
            additional_details (str, optional): Additional details about the address, could be particular building in a condo, or something else. 
                                                Defaults to None.
            gateway_token (str, optional): This is a gateway token handled entirely by Vindi. Defaults to None.
        Returns:
            bool: Return True that the billing information was updated.
        """

        # automatically sets the country to 'BR' if the country is None, we use this now but might change
        # when internationalizing the platform
        country = country if country else 'BR'

        billing_service = cls(company_id)
        for current_company_charge in current_company_charges:
            billing_service.charge_service.update_or_create(
                current_company_charge.charge_name, 
                current_company_charge.user_id, 
                current_company_charge.quantity, 
                push_updates=False
            )
        billing_service.payment_service.update_address_and_company_info(
            cnpj, zip_code, street, state, number, neighborhood, country, 
            city, additional_details, push_updates=False
        )
        billing_service.payment_service.update_payment(payment_method_type_id, invoice_date_type_id, emails, gateway_token=gateway_token, push_updates=True)
        return True
        
    @classmethod
    @transaction.atomic
    def create_on_onboarding(cls, company_id, user_id):
        billing_service = cls(company_id)
        billing_service.create_company(push_updates=False)
        billing_service.create_user(user_id=user_id, push_updates=False)
        billing_service.charge_service.push_updates()
        return True
        