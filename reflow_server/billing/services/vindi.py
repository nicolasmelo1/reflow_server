from django.conf import settings
from django.db import transaction

from rest_framework import status

from reflow_server.authentication.models import Company
from reflow_server.billing.models import CompanyInvoiceMails, CompanyBilling


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
        self.company = Company.billing_.company_by_company_id(company_id)
        self.company_billing = CompanyBilling.objects.filter(company_id=company_id).first()

        from reflow_server.billing.externals import VindiExternal
        from reflow_server.billing.services.charge import ChargeService

        self.charge_service = ChargeService(company_id, self.company_billing)
        self.vindi_external = VindiExternal()

        self.vindi_plan_id = self.company_billing.vindi_plan_id
        self.vindi_client_id = self.company_billing.vindi_client_id
        self.vindi_product_id = self.company_billing.vindi_product_id
        self.vindi_payment_profile_id = self.company_billing.vindi_payment_profile_id
        self.vindi_signature_id = self.company_billing.vindi_signature_id
    # ------------------------------------------------------------------------------------------
    @property
    def __total(self):
        """
        We use this so this service can work independently from external services.

        If we just want to update some company inside vindi we can just use this service instead
        of depending on needing to call BillingService first and then this Service. The problem is that 
        with this solution circular imports might occur because we use the VindiService in BillingService, 
        so we need to import the BillingService inside this method.

        Important: it automatically caches the total value so it doesn't need to get and calculate the total everytime. 
        Always calculating can lead to inconsistencies, with this we calculate just once and use this for all the values.
        """
        if hasattr(self, '_cache_total'):
            return self._cache_total
        else:
            self._cache_total = self.charge_service.get_total_data_from_custom_charge_quantity(self.company_billing.plan_id, []).total
            return self._cache_total
    # ------------------------------------------------------------------------------------------
    def __get_correct_payment_method_type(self, payment_method):
        if payment_method:
            return settings.VINDI_PAYMENT_METHODS.get(payment_method, payment_method)
        else:
            return None
    # ------------------------------------------------------------------------------------------
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
                    self.vindi_client_id, self.company_billing.street, self.company_billing.number, 
                    self.company_billing.zip_code, self.company_billing.neighborhood, 
                    self.company_billing.city, self.company_billing.state, self.company_billing.country, 
                    self.company.name, emails[0].email, self.company_billing.cnpj,
                    [email.email for email in emails[1:]]
                )
            else: 
                response = self.vindi_external.create_client(
                    self.company_billing.street, self.company_billing.number, 
                    self.company_billing.zip_code, self.company_billing.neighborhood, 
                    self.company_billing.city, self.company_billing.state, self.company_billing.country, 
                    self.company.name, emails[0].email, self.company_billing.cnpj,
                    [email.email for email in emails[1:]]
                )
        status_code = response.status_code if response and response.status_code else None
        self.vindi_client_id = response.json().get('customer', {}).get('id', self.vindi_client_id) if response else self.vindi_client_id
        return (status_code, self.vindi_client_id)
    # ------------------------------------------------------------------------------------------
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
        status_code = response.status_code if response and response.status_code else None
        self.vindi_product_id = response.json().get('product', {}).get('id', self.vindi_product_id) if response else self.vindi_product_id
        return (status_code, self.vindi_product_id)
    # ------------------------------------------------------------------------------------------
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
                'plan_of_company_{}'.format(self.company.id),
                self.company_billing.invoice_date_type.date
            )
        else:
            response = self.vindi_external.create_plan(
                'plan_of_company_{}'.format(self.company.id),
                self.company_billing.invoice_date_type.date
            )

        status_code = response.status_code if response and response.status_code else None
        self.vindi_plan_id = response.json().get('plan', {}).get('id', self.vindi_plan_id) if response else self.vindi_plan_id
        return (status_code, self.vindi_plan_id)
    # ------------------------------------------------------------------------------------------
    def __create_payment_profile(self, gateway_token):
        """
        We don't handle anything about credit card information in our side since this is REALLY REALLY sensitive and can lead
        to problems if we don't follow many rules about transactioning credit card data.
        
        For further reference read:
        https://atendimento.vindi.com.br/hc/pt-br/articles/115009609107-Como-eu-cadastro-perfis-de-pagamento-

        Args:
            gateway_token (str): This is handled by vindi, this token is an unique id that holds the creditcard data. This is handled
                                 entirely by Vindi.

        Returns:
            tuple: Tuple containing the `status_code` as first argument and the created `vindi_payment_profile_id`.
        """
        response = None

        if gateway_token:
            response = self.vindi_external.create_payment_profile(
                gateway_token,
                self.vindi_client_id,
                self.__get_correct_payment_method_type(self.company_billing.payment_method_type.name)
            )

        # this works differently because it's not always that we want to create a payment profile, so it returns always 200
        status_code = response.status_code if response and response.status_code else 200
        self.vindi_payment_profile_id = response.json().get('payment_profile', {}).get('id', self.vindi_payment_profile_id) if response else self.vindi_payment_profile_id
        return (status_code, self.vindi_payment_profile_id)
    # ------------------------------------------------------------------------------------------
    def __create_or_update_subscription(self):
        """
        We don't handle the billing internally, we let vindi handle subscription for us. This way we actually get locked somewhat in
        their implementation of subscriptions, but it's easier for us to implement. It also prevents us from having bigger operational costs.
        So some questions like: if the user changes the value in the day after he's paying he'll pay the new value or the old value in this
        invoice? If the user change the date he wants to be billed a week before being billed he'll pay in the previous or the new date?

        And etc. Are actually handled and need to be responded by Vindi itself. We don't handle it inside of Reflow.

        When we are updating the subscription we don't change the price directly in the subscription but instead we change it in the product_items passing the id

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
                self.__get_correct_payment_method_type(self.company_billing.payment_method_type.name),
                self.company_billing.invoice_date_type.date, self.__total
            )
            if response and response.status_code == 200 and response.json().get('subscription', {}).get('product_items', []):
                self.__update_product_item(response.json().get('subscription', {}).get('product_items', [])[0]['id'])
        else:
            response = self.vindi_external.create_subscription(
                self.vindi_plan_id, self.vindi_client_id, self.vindi_product_id,
                self.__get_correct_payment_method_type(self.company_billing.payment_method_type.name),
                self.company_billing.invoice_date_type.date, self.__total
            )
        status_code = response.status_code if response and response.status_code else None
        self.vindi_signature_id = response.json().get('subscription', {}).get('id', self.vindi_signature_id) if response else self.vindi_signature_id
        return (status_code, self.vindi_signature_id)
    # ------------------------------------------------------------------------------------------
    def __update_product_item(self, product_item_id):
        """
        This is used so we can update the subscription pricing in vindi payment gateway.
        This is only used when we update a subscription.

        Args:
            product_item_id (int): The vindi_product_item_id. Usually, at least in reflow what happens is that a 
                                   singe subscription have just one product_item that is the full price.

        Raises:
            ConnectionError: Something happened while updating the user subscription data
        """
        response = self.vindi_external.update_product_item(product_item_id, self.vindi_product_id, self.vindi_signature_id, self.__total)
        if not response or response.status_code != 200:
            raise ConnectionError('Something happened while updating the user subscription data')
    # ------------------------------------------------------------------------------------------
    def get_credit_card_info(self):
        """
        Gets the credit card information from the payment_profile_id of the company.

        Returns:
            dict: returns a dict containing all of the credit card info with the following keys:
                  - `card_number_last_four`: last four digits of the credit card
                  - `card_expiration`: the expiration date of the credit card.
                  - `credit_card_code`: this is a string representing from which credit card company is this 
                    credit card from
                  - `payment_company_name`: The company of the credit card.
        """
        if self.vindi_payment_profile_id:
            return self.vindi_external.get_payment_profile(self.vindi_payment_profile_id)
        else:
            return None
    # ------------------------------------------------------------------------------------------           
    def delete_payment_profile(self):
        """
        As the name suggests, deletes the payment profile from vindi. This is usually used when the user wants to delete his credit card.

        Returns:
            bool: returns True or False whether the delete action was successful or not.
        """
        if self.vindi_payment_profile_id in [None, '']:
            return True
        else:
            if self.vindi_external.delete_payment_profile(self.vindi_payment_profile_id).status_code == 200:
                self.company_billing.vindi_payment_profile_id = None
                self.company_billing.save()
                return True
            else:
                return False
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def create_or_update(self, gateway_token=None):
        """
        This method is responsible for create or updating a client in Vindi. As you see down below we actually create a pipeline of insertion.
        As mentioned in Vindi docs, everything should follow this exact order.

        1 - Create or update the client
        2 - Create or update the product
        3 - Create or update the plan
        4 - Create the payment_profile (only creates we never update)
        5 - Create or update the subscription

        Args:
            gateway_token (str, optional): This is handled by vindi, this token is an unique id that holds the creditcard data. This is handled
                                 entirely by Vindi but we need it to save the credit card in the database. Defaults to None.

        Returns:
            bool: Returns True if everything went smoothly and fine, and False if any request faced a problem.
        """
        self.__create_or_update_client()
        self.__create_or_update_product()
        self.__create_or_update_plan()
        self.__create_payment_profile(gateway_token)
        self.__create_or_update_subscription()
  
        self.company_billing.vindi_plan_id = self.vindi_plan_id
        self.company_billing.vindi_client_id = self.vindi_client_id
        self.company_billing.vindi_product_id = self.vindi_product_id
        self.company_billing.vindi_payment_profile_id = str(getattr(self, 'vindi_payment_profile_id', None))
        self.company_billing.vindi_signature_id = getattr(self, 'vindi_signature_id', None)
        self.company_billing.save()
        return True
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def handle_webhook(data):
        """
        IMPORTANT: in order to make it better we should move this code to the worker so in case it fails we can retry it again, and we have
        fallback access to know when it fails.

        This is responsible for handling Vindi webhook requests. You just need to send the data recieved and this function takes 
        care of the rest.

        Here we only listen to `subscription_canceled` event so we deactivate a Company, we listen to `subscription_reactivated` so
        we reactivate a Company and last but not least `bill_paid` this way we add the payment data in our database.

        For further reference: https://atendimento.vindi.com.br/hc/pt-br/articles/203305800-O-que-s%C3%A3o-e-como-funcionam-os-Webhooks-

        Args:
            data (dict): The json of the event so we can parse it here. Since it can change many times 
                         we parse it here in the service and not in the view.
        """
        event = data.get('event', {}).get('type', '')
        data = data.get('event', {}).get('data', {})
        if event in list(settings.VINDI_ACCEPTED_WEBHOOK_EVENTS.keys()) and data.get(settings.VINDI_ACCEPTED_WEBHOOK_EVENTS[event], None):
            data = data[settings.VINDI_ACCEPTED_WEBHOOK_EVENTS[event]]

            if event in ['subscription_canceled', 'charge_rejected', 'charge_canceled']:
                company_billing = CompanyBilling.objects.filter(vindi_signature_id=data.get('id', -1)).first()
                if company_billing and not company_billing.is_supercompany:
                    Company.billing_.update_is_active_by_company_id(company_billing.company.id, False)

            elif event == 'subscription_reactivated':
                company_billing = CompanyBilling.objects.filter(vindi_signature_id=data.get('id', -1)).first()
                if company_billing and not company_billing.is_supercompany:
                    Company.billing_.update_is_active_by_company_id(company_billing.company.id, True)

            elif event == 'bill_paid':
                from reflow_server.billing.services.charge import ChargeService
                from reflow_server.billing.services import BillingService

                vindi_customer_id = data.get('customer', {}).get('id', None)
                total_value = data.get('amount', 0)
                attempt_count = 0
                charges = data.get('charges', [{}])
                if isinstance(charges, list) and len(charges) > 0:
                    attempt_count = charges[0].get('attempt_count', 0)

                company_id = CompanyBilling.billing_.company_id_by_vindi_client_id(vindi_customer_id)
                ChargeService.add_new_company_charge(company_id, total_value, attempt_count)
            elif event == 'bill_created':
                from reflow_server.billing.services.charge import ChargeService
                vindi_customer_id = data.get('customer', {}).get('id', None)
                total_value = data.get('amount', 0)
                ChargeService.add_new_company_charge_sent(vindi_customer_id, total_value)