from django.db import transaction

from reflow_server.billing.models import DiscountByIndividualNameForCompany, CurrentCompanyCharge, CompanyBilling, \
    PartnerDefaultAndDiscounts, DiscountCoupon, CompanyCoupons
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
        self.company_id = company_id
        self.company_billing = CompanyBilling.objects.filter(company_id=company_id).first()
        self.charge_service = ChargeService(company_id, self.company_billing)
        self.payment_service = PaymentService(company_id, self.company_billing)
    
    def remove_credit_card(self):
        return VindiService(self.company_id).delete_payment_profile()

    @transaction.atomic
    def update_charge(self, company_charge_data=[]):
        """
        Update only the charge information and update the billing, if no `current_company_charge` this means we are probably
        updating the charge information outside of the billing so we need to add it and push the updates to vindi. 

        When we are updating from the outside what we do is loop through all of the CurrentCompanyCharge and create a `CompanyChargeData`
        from each CurrentCompanyCharge instance. Then we use `validate_current_company_charges_and_create_new` function to create all of
        the missing `CompanyChargeData`. Last but not least we push the updates to vindi

        When updating from the inside what we do not loop the `CurrentCompanyCharge` instances and we do not push the updates
        to vindi.
        """
        current_company_charge_data = company_charge_data
        if len(company_charge_data) == 0:
            for current_company_charge in CurrentCompanyCharge.objects.filter(company_id=self.company_id):
                current_company_charge_data.append(
                    CompanyChargeData(
                        current_company_charge.individual_charge_value_type.name,
                        current_company_charge.quantity
                    )
                )
        current_company_charges_from_request = self.charge_service.validate_current_company_charges_and_create_new(current_company_charge_data)
        for current_company_charge in current_company_charges_from_request:
            self.charge_service.update_or_create(
                current_company_charge.individual_value_charge_name, 
                current_company_charge.quantity, 
                push_updates=False
            )
        if len(company_charge_data) == 0:
            self.charge_service.push_updates()
    
    def is_valid_company_invoice_emails(self, length_of_company_invoice_emails):
        return not (length_of_company_invoice_emails > 3 or length_of_company_invoice_emails < 1)

    def create_discount_by_individual_name_for_company_by_partner_name(self, partner_name):
        """
        From the Partner defaults and discounts update the DiscountByIndividualNameForCompany
        so we can use this discount on the company

        Args:
            partner_name (str): Be aware the name of the partner here must be the same defined in 
                                reflow_server.authentication.models.Company `partner` column

        Returns:
            bool: returns True indicating everything went fine
        """
        if partner_name not in [None, '']:
            partner_discounts = PartnerDefaultAndDiscounts.billing_.partner_default_and_discounts_by_partner_name(partner_name)
            for partner_discount in partner_discounts:
                if partner_discount.discount_value:
                    DiscountByIndividualNameForCompany.billing_.create(
                        partner_discount.individual_charge_value_type_id,
                        partner_discount.discount_value,
                        partner_name,
                        self.company_id
                    )
        return True

    def create_discount_coupon_for_company(self, discount_coupon_name):
        """
        Adds a new discount coupon to the company

        Args:
            discount_coupon_name (str): The name of the discount coupon
        """
        if discount_coupon_name:
            discount_coupon_id = DiscountCoupon.billing_.discount_coupon_id_by_coupon_name(discount_coupon_name)
            if discount_coupon_id:
                CompanyCoupons.billing_.create(self.company_id, discount_coupon_id)
            
    def __send_update_billing_events(self):
        """
        Sends the events to the users after the billing was updated. 
        So they can update their data.
        """
        from reflow_server.billing.events import BillingEvents

        BillingEvents().send_updated_billing(self.company_id)

    @transaction.atomic
    def update_billing_information(self, payment_method_type_id, invoice_date_type_id, emails, 
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

        self.update_charge(current_company_charges)
        self.payment_service.update_address_and_company_info(
            cnpj, zip_code, street, state, number, neighborhood, country, 
            city, additional_details, push_updates=False
        )
        self.payment_service.update_payment(payment_method_type_id, invoice_date_type_id, emails, gateway_token=gateway_token, push_updates=True)
        self.__send_update_billing_events()
        return True
        
    @classmethod
    @transaction.atomic
    def create_on_onboarding(cls, company_id, user_id, partner_name=None, discount_coupon_name=None):
        """
        Creates the company and the first user on the billing. This is for onboarding only.

        Args:
            company_id (int): The id of the company you just created
            user_id (id): The id of the 

        Returns:
            bool: returns True to show everything went alright
        """
        billing_service = cls(company_id)
        billing_service.company_billing = CompanyBilling.objects.create(company_id=company_id)
        billing_service.charge_service = ChargeService(company_id, billing_service.company_billing)
        billing_service.create_discount_by_individual_name_for_company_by_partner_name(partner_name)
        billing_service.create_discount_coupon_for_company(discount_coupon_name)
        billing_service.update_charge()
        return True
        