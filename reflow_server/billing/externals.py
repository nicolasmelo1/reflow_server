from django.conf import settings

from reflow_server.core import externals
from reflow_server.billing.serializers import VindiClientSerializer, VindiSubscriptionSerializer, \
    VindiProductSerializer


class VindiExternal(externals.External):
    host = settings.VINDI_API_HOST
    secure = False
    basic_auth = ('knbtmIJp7smiSzQdThuAquX80aHCGDV9VO2L6_mYOuU', '')

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
        self.post('/customers', serializer.data)
    
    def update_client(self, address_street, address_number, 
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

        self.put('/customers', serializer.data)

    def create_product(self, product_name, product_description, price):
        serializer = VindiProductSerializer(
            product_name, product_description, price
        )

        self.post('/products', serializer.data)

    def update_product(self, product_name, product_description, price):
        serializer = VindiProductSerializer(
            product_name, product_description, price
        )

        self.put('/products', serializer.data)

    def create_subscription(self, vindi_plan_id, vindi_client_id, vindi_product_id, 
                            payment_method_type, invoice_date_type, price):
        serializer = VindiSubscriptionSerializer(
            vindi_plan_id, vindi_client_id, vindi_product_id, 
            payment_method_type, invoice_date_type, price
        )

        self.post('/subscriptions', serializer.data)

    def update_subscription(self, vindi_plan_id, vindi_client_id, vindi_product_id, 
                            payment_method_type, invoice_date_type, price):
        serializer = VindiSubscriptionSerializer(
            vindi_plan_id, vindi_client_id, vindi_product_id, 
            payment_method_type, invoice_date_type, price
        )

        self.put('/subscriptions', serializer.data)

    

    