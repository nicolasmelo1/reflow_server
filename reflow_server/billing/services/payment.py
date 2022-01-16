from reflow_server.authentication.models import Company, UserExtended
from reflow_server.billing.models import BillingPlan, CompanyInvoiceMails, PaymentMethodType, InvoiceDateType
from reflow_server.billing.services.vindi import VindiService


class PaymentService:
    def __init__(self, company_id, company_billing):
        """
        This updates the data used for the company, in other words, the CompanyBilling instance.
        This service holds everything about the data needed for making payments, it's not about permissions like
        ChargeService.

        Args:
            Args:
            company (int): The company_id we are changing
            company_billing (reflow_server.billing.models.CompanyBilling): This is a CompanyBilling instance, 
                                                                           it is similar to Company but holds all
                                                                           of the billing data for a particular company
        """
        self.company_id = company_id
        self.company_billing = company_billing
    
    def push_updates(self, gateway_token=None):
        """
        Sends the updates made here in our billing service to our Payment Gateway, so the Payment
        Gateway can work with new data.
    
        gateway_token (str, optional): Gateway token is something that is handled by Vindi payment gateway. Defaults to None.
        """
        if not self.company_billing.is_supercompany and self.company_billing.is_paying_company:
            vindi_service = VindiService(self.company_id)
            vindi_service.create_or_update(gateway_token=gateway_token)

    def update_address_and_company_info(self, cnpj, zip_code, street, state, number, neighborhood, 
                                        country, city, additional_details=None, push_updates=True):
        self.company_billing.cnpj = cnpj
        self.company_billing.additional_details = additional_details
        self.company_billing.zip_code = zip_code
        self.company_billing.street = street
        self.company_billing.state = state
        self.company_billing.number = number
        self.company_billing.neighborhood = neighborhood
        self.company_billing.country = country
        self.company_billing.city = city
        self.company_billing.is_paying_company = True
        self.company_billing.save()

        if push_updates:
            self.push_updates()
        return True
    
    def update_payment(self, plan_id, payment_method_type_id, invoice_date_type_id, emails, gateway_token=None, push_updates=True):
        """
        Updates the payment data of a company

        Args:
            payment_method_type_id (int): the id of a single reflow_server.billing.models.PaymentMethodType model.
            invoice_date_type_id (int): the id of a single reflow_server.billing.models.InvoiceDateType model.
            emails (list(str)): A list of strings where all of the strings are a single email.
            gateway_token (str, optional): Gateway token is something that is handled by Vindi payment gateway. Defaults to None.
        """
        CompanyInvoiceMails.objects.filter(company_id=self.company_id).delete()
        CompanyInvoiceMails.objects.bulk_create([
            CompanyInvoiceMails(email=email, company_id=self.company_id) for email in emails
        ])
        self.company_billing.plan_id = plan_id
        self.company_billing.payment_method_type_id = payment_method_type_id
        self.company_billing.invoice_date_type_id = invoice_date_type_id
        self.company_billing.save()
        self.__check_if_selected_plan_is_free(plan_id)
        if push_updates:
            self.push_updates(gateway_token)
        return True

    def remove_credit_card(self):
        """
        Removes the credit card of the company from our payment gateway, the payment gateway is
        also responsible for updating the company info.
        """
        if self.company_billing.is_paying_company:
            vindi_service = VindiService(self.company_id)
            return vindi_service.delete_payment_profile()
        else:
            return False

    def __check_if_selected_plan_is_free(self, plan_id):
        """
        Will check if the selected plan is the Freemium plan and then we remove the users and only let the admin access, otherwise
        we will enable everyone that was disabled.
        """
        is_plan_id_freemium = BillingPlan.billing_.is_plan_id_freemium(plan_id)
        if is_plan_id_freemium:
            UserExtended.billing_.deactivate_all_accounts_except_oldest_by_company_id(self.company_id)
        else:
            UserExtended.billing_.reactivate_all_accounts_by_company_id(self.company_id)