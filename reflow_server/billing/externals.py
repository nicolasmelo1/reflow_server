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
        response = self.get('/payment_profiles/{}'.format(vindi_payment_profile_id)).json()
        credit_card_info = {
            'card_number_last_four': response.get('payment_profile', {}).get('card_number_last_four', ''),
            'card_expiration': response.get('payment_profile', {}).get('card_expiration', ''),
            'credit_card_code': response.get('payment_profile', {}).get('payment_company', {}).get('code', ''),
            'payment_company_name': response.get('payment_profile', {}).get('payment_company', {}).get('name', '')
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
    