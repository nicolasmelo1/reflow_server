from reflow_server.authentication.models import Company
from reflow_server.billing.models import CompanyInvoiceMails, PaymentMethodType, InvoiceDateType
from reflow_server.billing.services.vindi import VindiService


class PaymentService:
    def __init__(self, company):
        self.company = company
    
    def push_updates(self, gateway_token=None):
        """
        Sends the updates made here in our billing service to our Payment Gateway, so the Payment
        Gateway can work with new data.
    
        gateway_token (str, optional): Gateway token is something that is handled by Vindi payment gateway. Defaults to None.
        """
        if not self.company.is_supercompany and self.company.is_paying_company:
            vindi_service = VindiService(self.company.id)
            vindi_service.create_or_update(gateway_token=gateway_token)

    def update_address_and_company_info(self, cnpj, zip_code, street, state, number, neighborhood, 
                                        country, city, additional_details=None, push_updates=True):
        self.company.cnpj = cnpj
        self.company.additional_details = additional_details
        self.company.zip_code = zip_code
        self.company.street = street
        self.company.state = state
        self.company.number = number
        self.company.neighborhood = neighborhood
        self.company.country = country
        self.company.city = city
        self.company.is_paying_company = True
        self.company.save()

        if push_updates:
            self.push_updates()
        return True

    def update_payment(self, payment_method_type_id, invoice_date_type_id, emails, gateway_token=None, push_updates=True):
        """
        updates the payment data of a company

        Args:
            payment_method_type_id (int): the id of a single reflow_server.billing.models.PaymentMethodType model.
            invoice_date_type_id (int): the id of a single reflow_server.billing.models.InvoiceDateType model.
            emails (list(str)): A list of strings where all of the strings are a single email.
            gateway_token (str, optional): Gateway token is something that is handled by Vindi payment gateway. Defaults to None.
        """
        CompanyInvoiceMails.objects.filter(company_id=self.company.id).delete()
        CompanyInvoiceMails.objects.bulk_create([
            CompanyInvoiceMails(email=email, company_id=self.company.id) for email in emails
        ])
        self.company.payment_method_type_id = payment_method_type_id
        self.company.invoice_date_type_id = invoice_date_type_id
        self.company.save()
        if push_updates:
            self.push_updates(gateway_token)
        return True

    def remove_credit_card(self):
        """
        Removes the credit card of the company from our payment gateway, the payment gateway is
        also responsible for updating the company info.
        """
        if self.company.is_paying_company:
            vindi_service = VindiService(self.company.id)
            return vindi_service.delete_payment_profile()
        else:
            return False

