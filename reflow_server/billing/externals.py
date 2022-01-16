from django.conf import settings

from reflow_server.core import externals
from reflow_server.billing.serializers.vindi import VindiClientSerializer, VindiSubscriptionSerializer, \
    VindiProductSerializer, VindiPaymentProfileSerializer, VindiPlanSerializer, VindiProductItemsSerializer


class VindiExternal(externals.External):
    host = settings.VINDI_API_HOST
    secure = False
    basic_auth = (settings.VINDI_PRIVATE_API_KEY, '')

    def create_client(self, address_street, address_number, 
                      address_zip_code, address_neighborhood, 
                      address_city, address_state, address_country, 
                      company_name, company_email, company_registry_code,
                      emails=list()):
        """
        This creates the client in the Vindi payment gateway. Each client for us is the company 
        (since we bill each company individually). So the company is bound to the vindi client.
        The client holds information about the company so the address, following the zip_code the
        neighborhood and so on. With this we also bound the email of who to send the invoice and so on.

        Args:
            address_street (str): The street of the company
            address_number (int): The number of the company in the street
            address_zip_code (str): The zip_code of the company, where it is located.
            address_neighborhood (str): The neighborhood of where the company is located
            address_city (str): The city of where the company is located
            address_state (str): The state of the country of where the company is located. Should be in
                                 the ISO 3166-2 format. Example: SP
            address_country (str): The country where the company is located. This should be in ISO 3166-1 alpha-2
                                   format. Example: BR 
            company_name (str): The name of the company, this is used so we can diferentiate between 
                                the clients in vindi.
            company_email (str): This is the e-mail we want to send the invoice to
            company_registry_code (str): The company CNPJ. In Brazil each company have a CNPJ and it is obligatory
                                         for us to send the invoice to the user
            emails (list(str), optional): Sometimes you want to send the invoice to more than just one user. So you send
                                          a copy of the invoice e-mail to more users. Defaults to list().

        Returns:
            requests.Response: Reference on what it returns https://vindi.github.io/api-docs/dist/#/customers/postV1Customers
        """
        serializer = VindiClientSerializer(
            address_street, address_number, address_zip_code, 
            address_neighborhood, address_city, address_state, 
            address_country, company_name, company_email, 
            company_registry_code, emails
        )
        return self.post('/customers', serializer.data)
    
    def update_client(self, vindi_client_id, address_street, address_number, 
                      address_zip_code, address_neighborhood, 
                      address_city, address_state, address_country, 
                      company_name, company_email, company_registry_code,
                      emails=list()):
        """
        Same as `create_client`, except is that we update a client here. So we make a 
        PUT request and also need the `vindi_client_id` which is a parameter not needed 
        in the `create_client` method.

        Args:
            vindi_client_id (str): The client_id from vindi that we need to update.
            address_street (str): The street of the company
            address_number (int): The number of the company in the street
            address_zip_code (str): The zip_code of the company, where it is located.
            address_neighborhood (str): The neighborhood of where the company is located
            address_city (str): The city of where the company is located
            address_state (str): The state of the country of where the company is located. Should be in
                                 the ISO 3166-2 format. Example: SP
            address_country (str): The country where the company is located. This should be in ISO 3166-1 alpha-2
                                   format. Example: BR 
            company_name (str): The name of the company, this is used so we can diferentiate between 
                                the clients in vindi.
            company_email (str): This is the e-mail we want to send the invoice to
            company_registry_code (str): The company CNPJ. In Brazil each company have a CNPJ and it is obligatory
                                         for us to send the invoice to the user
            emails (list(str), optional): Sometimes you want to send the invoice to more than just one user. So you send
                                          a copy of the invoice e-mail to more users. Defaults to list().

        Returns:
            requests.Response: Reference on what it returns https://vindi.github.io/api-docs/dist/#/customers/putV1CustomersId
        """
        serializer = VindiClientSerializer(
            address_street, address_number, address_zip_code, 
            address_neighborhood, address_city, address_state, 
            address_country, company_name, company_email, 
            company_registry_code, emails
        )

        return self.put('/customers/{}'.format(vindi_client_id), serializer.data)

    def create_product(self, product_name, product_description, price):
        serializer = VindiProductSerializer(
            product_name, product_description, price
        )

        return self.post('/products', serializer.data)

    def update_product(self, vindi_product_id, product_name, product_description, price):
        serializer = VindiProductSerializer(
            product_name, product_description, price
        )

        return self.put('/products/{}'.format(vindi_product_id), serializer.data)

    def create_subscription(self, vindi_plan_id, vindi_client_id, vindi_product_id, 
                            payment_method_type, invoice_date_type, price):
        serializer = VindiSubscriptionSerializer(
            vindi_plan_id, vindi_client_id, vindi_product_id, 
            payment_method_type, invoice_date_type, price
        )

        return self.post('/subscriptions', serializer.data)

    def update_subscription(self, vindi_subscription_id, vindi_plan_id, vindi_client_id, 
                            vindi_product_id, payment_method_type, invoice_date_type, price):
        serializer = VindiSubscriptionSerializer(
            vindi_plan_id, vindi_client_id, vindi_product_id, 
            payment_method_type, invoice_date_type, price
        )

        return self.put('/subscriptions/{}'.format(vindi_subscription_id), serializer.data)

    def update_product_item(self, vindi_product_item_id, vindi_product_id, vindi_subscription_id, price):
        serializer = VindiProductItemsSerializer(
            vindi_product_id, vindi_subscription_id, price
        )

        return self.put('/product_items/{}'.format(vindi_product_item_id), serializer.data)

    def create_payment_profile(self, gateway_token, vindi_client_id, payment_method_type):
        serializer = VindiPaymentProfileSerializer(
            gateway_token, vindi_client_id, payment_method_type
        )

        return self.post('/payment_profiles', serializer.data)
    
    def delete_payment_profile(self, vindi_payment_profile_id):
        return self.delete('/payment_profiles/{}'.format(vindi_payment_profile_id))

    def get_payment_profile(self, vindi_payment_profile_id):
        response = self.get('/payment_profiles/{}'.format(vindi_payment_profile_id))
        if response != None:
            response_json = response.json()
        else:
            response_json = {}
        
        credit_card_info = {
            'card_number_last_four': response_json.get('payment_profile', {}).get('card_number_last_four', ''),
            'card_expiration': response_json.get('payment_profile', {}).get('card_expiration', ''),
            'credit_card_code': response_json.get('payment_profile', {}).get('payment_company', {}).get('code', ''),
            'payment_company_name': response_json.get('payment_profile', {}).get('payment_company', {}).get('name', '')
        }
        return credit_card_info

    def create_plan(self, plan_name, invoice_date_type):
        serializer = VindiPlanSerializer(
            plan_name, invoice_date_type
        )
        
        return self.post('/plans', serializer.data)

    def update_plan(self, vindi_plan_id, plan_name, invoice_date_type):
        serializer = VindiPlanSerializer(
            plan_name, invoice_date_type
        )
        
        return self.put('/plans/{}'.format(vindi_plan_id), serializer.data)
    