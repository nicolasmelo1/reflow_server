from django.conf import settings
from django.db import transaction

from reflow_server.authentication.models import Company
from reflow_server.billing.models import CompanyInvoiceMails


class VindiService:
    def __init__(self, company_id):
        """
        This service handles vindi payment gateway integration with reflow.

        Read this for reference:
        https://atendimento.vindi.com.br/hc/pt-br/sections/200712564-Desenvolvedores
        https://vindi.github.io/api-docs/dist/

        Args:
            company_id (int): The id of the company you want to handle in vindi gateway
        """
        from reflow_server.billing.externals import VindiExternal
        from reflow_server.billing.services import BillingService

        self.billing_service = BillingService(company_id)
        self.vindi_external = VindiExternal()

        self.company = Company.objects.filter(id=company_id).first()
        self.vindi_plan_id = self.company.vindi_plan_id
        self.vindi_client_id = self.company.vindi_client_id
        self.vindi_product_id = self.company.vindi_product_id
        self.vindi_payment_profile_id = self.company.vindi_payment_profile_id
        self.vindi_signature_id = self.company.vindi_signature_id

    @property
    def __total(self):
        """
        We use this so this service can work independently from external services.

        If we just want to update some company inside vindi we can just use this service instead
        of depending on needing to call BillingService first and then this Service. The problem is that 
        with this solution circular imports might occur because we use the VindiService in BillingService, 
        so we need to import the BillingService inside this method.

        Important, it automatically caches the total value so it doesn't need to get and calculate the total everytime. 
        Always calculating can lead to inconsistencies, with this we calculate just once and use this for all the values.
        """
        if hasattr(self, '_cache_total'):
            return self._cache_total
        else:
            self._cache_total = self.billing_service.get_total_data.total
            return self._cache_total

    def __get_correct_payment_method_type(self, payment_method):
        if payment_method:
            return settings.VINDI_PAYMENT_METHODS.get(payment_method, payment_method)
        else:
            return None

    def __create_or_update_client(self):
        """
        Creates or updates a single client in the vindi gateway. 
        If the company has a `vindi_client_id` already created we make an update, otherwise we create.
        It's important to understand that we only make an create or update action if we have any 
        reflow_server.billing.models.CompanyInvoiceMails defined for this particular company.
        Usually client in vindi holds all of the information about the client, in our reallity it means it must hold
        the information about the company.

        See this for further reference: https://vindi.github.io/api-docs/dist/?url=https://sandbox-app.vindi.com.br/api/v1/docs#/customers/postV1Customers

        Returns:
            tuple: Tuple containing the `status_code` as first argument and the created `vindi_client_id`.
        """
        emails = CompanyInvoiceMails.objects.filter(company=self.company)
        response = None

        if emails:
            if self.vindi_client_id:
                response = self.vindi_external.update_client(
                    self.vindi_client_id, self.company.street, self.company.number, 
                    self.company.zip_code, self.company.neighborhood, 
                    self.company.city, self.company.state, self.company.country, 
                    self.company.name, emails[0].email, self.company.cnpj,
                    [email.email for email in emails[1:]]
                )
            else: 
                response = self.vindi_external.create_client    (
                    self.company.street, self.company.number, 
                    self.company.zip_code, self.company.neighborhood, 
                    self.company.city, self.company.state, self.company.country, 
                    self.company.name, emails[0].email, self.company.cnpj,
                    [email.email for email in emails[1:]]
                )

        status_code = response.status_code if response else None
        self.vindi_client_id = response.json().get('customer', {}).get('id', self.vindi_client_id) if response else self.vindi_client_id
        return (status_code, self.vindi_client_id)

    def __create_or_update_product(self):
        """
        This method creates or updates products in vindi gateway. We only create if no product_id has been set for the company
        otherwise we update.
        Actually product is supposed to hold the products of the client for the subscription. To correctly use this we should add each product we offer in Vindi
        and then let Vindi handle the subscription we would just hold the ID of each product_id inside vindi.
        But as you might think we don't like to stay locked and like to handle stuff by ourselves. With this in mind what we actually do is calculate
        the total in our side and then create a product for each company with the total, this means that products in Vindi actually is the total for each company.
        But all of the calculations and how we handle each product we offer is handled by us internally inside of reflow.

        See this for further reference: https://vindi.github.io/api-docs/dist/?url=https://sandbox-app.vindi.com.br/api/v1/docs#/products

        Returns:
            tuple: Tuple containing the `status_code` as first argument and the created `vindi_product_id`.
        """
        response = None

        if self.vindi_product_id:
            response = self.vindi_external.update_product(
                self.vindi_product_id,
                'Valor total da {}'.format(self.company.name),
                'product_of_company_{}'.format(self.company.id),
                self.__total
            )
        else:
            response = self.vindi_external.create_product(
                'Valor total da {}'.format(self.company.name),
                'product_of_company_{}'.format(self.company.id),
                self.__total
            )
        status_code = response.status_code if response else None
        self.vindi_product_id = response.json().get('product', {}).get('id', self.vindi_product_id) if response else self.vindi_product_id
        return (status_code, self.vindi_product_id)

    def __create_or_update_plan(self):
        """
        This method creates or updates plans in vindi gateway. We only create if no plan_id has been set for the company
        otherwise we update.
        We were actually handling this if a single id since we only had 'monthly' subscription but decided to 
        start handling this here. This is responsible for setting the plans of the user, plans in vindi hold information about the
        plan we offer. The user is going to be billed monthly? Daily? or Yearly?. Plans define everything about the plan the user
        is in, plans is mostly about dates and periods.

        See this for further reference: https://vindi.github.io/api-docs/dist/?url=https://sandbox-app.vindi.com.br/api/v1/docs#/plans

        Returns:
            tuple: Tuple containing the `status_code` as first argument and the created `vindi_product_id`.
        """
        response = None

        if self.vindi_plan_id:
            response = self.vindi_external.update_plan(
                self.vindi_plan_id,
                'plan_of_company_{}',
                self.company.invoice_date_type.date
            )
        else:
            response = self.vindi_external.create_plan(
                'plan_of_company_{}',
                self.company.invoice_date_type.date
            )

        status_code = response.status_code if response else None
        self.vindi_plan_id = response.json().get('plan', {}).get('id', self.vindi_plan_id) if response else self.vindi_plan_id
        return (status_code, self.vindi_product_id)

    def __create_payment_profile(self, gateway_token):
        """
        We don't handle anything about credit card information in our side since this is REALLY REALLY sensitive and can lead
        to problems if we don't follow many rules about transactioning credit card data.
        
        For further reference read:
        https://atendimento.vindi.com.br/hc/pt-br/articles/115009609107-Como-eu-cadastro-perfis-de-pagamento-

        Args:
            gateway_token (str): This is handled by vindi, this token is an unique id that holds the creditcard data. This is handled
                                 entirely by Vindi but we need it to save the credit card in the database.

        Returns:
            tuple: Tuple containing the `status_code` as first argument and the created `vindi_payment_profile_id`.
        """
        response = None

        if gateway_token:
            response = self.vindi_external.create_payment_profile(
                gateway_token,
                self.vindi_client_id,
                self.__get_correct_payment_method_type(self.company.payment_method_type.name)
            )

        # this works differently because it's not always that we want to create a payment profile, so it returns always 200
        status_code = response.status_code if response else 200
        self.vindi_payment_profile_id = response.json().get('payment_profile', {}).get('id', self.vindi_payment_profile_id) if response else self.vindi_payment_profile_id
        return (status_code, self.vindi_payment_profile_id)

    def __create_or_update_subscription(self):
        """
        We don't handle the billing internally, we let vindi handle subscription for us. This way we actually get locked somewhat in
        their implementation of subscriptions, but it's easier for us to implement. It also prevents us from having bigger operational costs.
        So some questions like: if the user changes the value in the day after he's paying he'll pay the new value or the old value in this
        invoice? If the user change the date he wants to be billed a week before being billed he'll pay in the previous or the new date?

        And etc. Are actually handled and need to be responded by Vindi itself. We don't handle it inside of Reflow.

        For further reference about subscriptions in vindi read:
        https://atendimento.vindi.com.br/hc/pt-br/articles/204022814-Como-eu-decido-qual-%C3%A9-o-melhor-tipo-de-integra%C3%A7%C3%A3o-
        https://vindi.github.io/api-docs/dist/#/subscriptions
    
        Returns:
        tuple: Tuple containing the `status_code` as first argument and the created `vindi_payment_profile_id`.
        """
        response = None

        if self.vindi_signature_id:
            response = self.vindi_external.update_subscription(
                self.vindi_signature_id, self.vindi_plan_id, self.vindi_client_id, self.vindi_product_id, 
                self.__get_correct_payment_method_type(self.company.payment_method_type.name),
                self.company.invoice_date_type.date, self.__total
            )
        else:
            response = self.vindi_external.create_subscription(
                self.vindi_plan_id, self.vindi_client_id, self.vindi_product_id,
                self.__get_correct_payment_method_type(self.company.payment_method_type.name),
                self.company.invoice_date_type.date, self.__total
            )
        status_code = response.status_code if response else 200
        self.vindi_signature_id = response.json().get('subscription', {}).get('id', self.vindi_signature_id) if response else self.vindi_signature_id
        return (status_code, self.vindi_signature_id)

    @transaction.atomic
    def update(self, gateway_token=None):
        pipeline = [
            self.__create_or_update_client(),   
            self.__create_or_update_product(),
            self.__create_or_update_plan(),
            self.__create_payment_profile(gateway_token),
            self.__create_or_update_subscription()
        ]
        
        if any([response[0] != 200 for response in pipeline]):
            return False
        else:
            self.company.vindi_plan_id = self.vindi_plan_id
            self.company.vindi_client_id = self.vindi_client_id
            self.company.vindi_product_id = self.vindi_product_id
            self.company.vindi_payment_profile_id = self.vindi_payment_profile_id
            self.company.vindi_signature_id = self.vindi_signature_id
            self.company.save()
            return True
        