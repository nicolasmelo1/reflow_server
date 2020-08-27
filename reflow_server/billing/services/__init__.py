from django.db import transaction
from django.db.models import Q

from reflow_server.authentication.models import Company, UserExtended
from reflow_server.billing.models import IndividualChargeValueType, CurrentCompanyCharge
from reflow_server.billing.services.data import CompanyChargeData
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

    @transaction.atomic
    def create_user(self, user_id):
        """
        Used for when creating a new user only, when updating you should use `.update_user()` method.
        It just loops for each 'charge_value_names' passing only the name as parameter, this way we always force to use the defauld value.

        Args:
            user_id (int): Id of the newly created user.

        Returns:
            list(reflow_server.billing.models.CurrentCompanyCharge): This data is a list of the instances of the newly created CurrentCompanyCharge.
                                                                     each item on the list represents each row inserted on the database for this user.
        """
        charge_value_names = ['per_user', 'per_chart_company', 'per_chart_user']
        self.charge_service.create(charge_value_names, user_id=user_id, push_updates=False)
        return self.charge_service.push_updates()

    @transaction.atomic
    def create_company(self):
        """
        Used for when creating a new company only, when updating you should use `.update()` method directly.
        It just loops for each 'charge_value_names' passing only the name as parameter, this way we always force to use the defauld value.

        Returns:
            list(reflow_server.billing.models.CurrentCompanyCharge): This data is a list of the instances of the newly created CurrentCompanyCharge.
                                                                     each item on the list represents each row inserted on the database.
        """
        charge_value_names = ['per_gb']
        self.charge_service.create(charge_value_names, push_updates=False)
        return self.charge_service.push_updates()

    def create_new_charge_value_for_a_individual_charge_type(self, individual_charge_value_type):
        """
        This is used in conjunction with `validate_current_company_charges_and_create_new` function.
        When we validate, if the condition is not set we create a new charge to the user.

        Args:
            individual_charge_value_type (reflow_server.billing.models.IndividualChargeValueType): The individual
            charge to be created, this way we can know if it is a user type or a company type. And can handle it
            accordingly.

        Returns:
            list(reflow_server.billing.services.data.CompanyChargeData): a list of CompanyChargeData created.
        """
        created_company_charges = []

        def get_quantity(user):
            current_quantity_for_this_individual_value_type = CurrentCompanyCharge.objects.filter(company_id=self.company.id, individual_charge_value_type=individual_charge_value_type).values_list('quantity', flat=True).first()
            if current_quantity_for_this_individual_value_type:
                quantity = current_quantity_for_this_individual_value_type
            else:
                quantity = individual_charge_value_type.default_quantity if individual_charge_value_type.default_quantity else 0
            return quantity

        if individual_charge_value_type.charge_type.name == 'user':
            for user in UserExtended.billing_.users_active_by_company_id(self.company.id):
                created_company_charges.append(CompanyChargeData(individual_charge_value_type.name, get_quantity(user), user.id))
        else:
            created_company_charges.append(CompanyChargeData(individual_charge_value_type.name, get_quantity(None)))
        return created_company_charges

    def validate_current_company_charges_and_create_new(self, current_company_charges):
        """
        This function is used to prevent frauds if the user opens the console and tries to insert company_charges not by the front-end
        but directly by the api.

        current_company_charges is usually an list, what happens is that on the front end we actually can prevent the user from some unwanted behaviour
        but on the backend we can't prevent it.

        What we are trying to prevent is: if for some reason a individual_charge_value_type is not created for a particular user or for the company
        we need to force its creation.

        Args:
            current_company_charges (list(reflow_server.billing.services.data.CompanyChargeData)): A list of CompanyChargeData

        Returns:
            list(reflow_server.billing.services.data.CompanyChargeData): A new list of CompanyChargeData
        """
        new_current_company_charges = []
        validate_current_company_charges = {}
        all_individual_charge_value_types = IndividualChargeValueType.objects.all()
        for current_company_charge in current_company_charges:
            validate_current_company_charges[current_company_charge.charge_name] = validate_current_company_charges.get(current_company_charge.charge_name, []) + [current_company_charge.user_id]
        # gets the difference of what was defined on the request and all of the others.
        difference_between_charge_value_types_defined_and_existent = list(set(all_individual_charge_value_types.values_list('name', flat=True)).difference(list(validate_current_company_charges.keys())))
        users_in_company = list(UserExtended.billing_.user_ids_active_by_company_id(self.company.id))

        # we loop though each individual_charge_value type and check for three conditions: 
        # 1 - The value of individual_charge_value_type.name was not defined on the current_company_charges list
        # 2 - The number of active users and the user_ids defined in each individual_charge_value_type.name doesn't match
        # 3 - We filter the current_company_charges of this individual_charge_value_type.name and use it
        for individual_charge_value_type in all_individual_charge_value_types:
            if individual_charge_value_type.name in difference_between_charge_value_types_defined_and_existent:    
                new_current_company_charges = new_current_company_charges + self.create_new_charge_value_for_a_individual_charge_type(individual_charge_value_type)
            elif individual_charge_value_type.charge_type.name == 'user' and \
                [user_in_company for user_in_company in users_in_company if user_in_company not in validate_current_company_charges.get(individual_charge_value_type.name, [])]:
                new_current_company_charges = new_current_company_charges + self.create_new_charge_value_for_a_individual_charge_type(individual_charge_value_type)
            else:
                new_current_company_charges = new_current_company_charges + \
                    [current_company_charge for current_company_charge in current_company_charges 
                    if current_company_charge.charge_name == individual_charge_value_type.name]

        return new_current_company_charges
    
    def is_valid_company_invoice_emails(self, length_of_company_invoice_emails):
        return not (length_of_company_invoice_emails > 3 or length_of_company_invoice_emails < 1)

    def __send_update_billing_events(self):
        """
        Sends the events to the users after the billing was updated. 
        So they can update their data.
        """
        from reflow_server.billing.events import BillingEvents

        BillingEvents().send_updated_billing(self.company.id)

    @transaction.atomic
    def update_billing(self, payment_method_type_id, invoice_date_type_id, emails, 
                       current_company_charges, cnpj, zip_code, street, state, 
                       number, neighborhood, country, city, additional_details=None, gateway_token=None):
        """
        Updates billing, so this is a factory method that automatically updates the payment data and also the charge data and pushes it
        to the payment gateway.

        To understand how we bill for dashboard charts go to: reflow_server.dashboard.services.permissions.DashboardPermissionsService

        Args:
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

        current_company_charges_from_request = self.validate_current_company_charges_and_create_new(current_company_charges)
        for current_company_charge in current_company_charges_from_request:
            self.charge_service.update_or_create(
                current_company_charge.charge_name, 
                current_company_charge.user_id, 
                current_company_charge.quantity, 
                push_updates=False
            )
        self.charge_service.remove_charge_values_from_removed_users()
        
        self.payment_service.update_address_and_company_info(
            cnpj, zip_code, street, state, number, neighborhood, country, 
            city, additional_details, push_updates=False
        )
        self.payment_service.update_payment(payment_method_type_id, invoice_date_type_id, emails, gateway_token=gateway_token, push_updates=True)
        self.__send_update_billing_events()
        return True
        
    @classmethod
    @transaction.atomic
    def create_on_onboarding(cls, company_id, user_id):
        """
        Creates the company and the first user on the billing. This is for onboarding only.

        Args:
            company_id (int): The id of the company you just created
            user_id (id): The id of the 

        Returns:
            bool: returns True to show everything went alright
        """
        billing_service = cls(company_id)
        billing_service.create_company()
        billing_service.create_user(user_id=user_id)
        return True
        