from rest_framework import serializers

from reflow_server.billing.relations import VindiClientAddressRelation, VindiClientMetadataRelation, \
    VindiSubscriptionProductItemRelation, VindiPricingSchemaRelation


class VindiClientSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    address = VindiClientAddressRelation()
    registry_code = serializers.CharField(allow_null=True)
    metadata = VindiClientMetadataRelation()

    def __init__(self, address_street, address_number, address_zip_code, 
                 address_neighborhood, address_city, address_state, 
                 address_country, company_name, company_email, 
                 company_registry_code, emails, *args, **kwargs):
        kwargs['data'] = {
            'name': company_name,
            'email': company_email,
            'address': {
                'street': address_street,
                'number': address_number,
                'zipcode': address_zip_code,
                'neighborhood': address_neighborhood,
                'city': address_city,
                'state': address_state,
                'country': address_country
            },
            'registry_code': company_registry_code,
            'metadata': {
                '_cc_email': emails
            }
        }

        super(VindiClientSerializer, self).__init__(**kwargs)
        self.is_valid()


class VindiSubscriptionSerializer(serializers.Serializer):
    plan_id = serializers.IntegerField()
    customer_id = serializers.IntegerField()
    payment_method_type = serializers.CharField()
    billing_trigger_type = serializers.CharField(default='day_of_month')
    billing_trigger_day = serializers.IntegerField()
    billing_cycles = serializers.NullBooleanField(default=None)
    product_items = VindiSubscriptionProductItemRelation(many=True)

    def __init__(self, vindi_plan_id, vindi_client_id, vindi_product_id, 
                 payment_method_type, invoice_date_type, price, *args, **kwargs):
        kwargs['data'] = {
            'plan_id': vindi_plan_id,
            'customer_id': vindi_client_id,
            'payment_method_code': payment_method_type,
            'billing_trigger_day': invoice_date_type,
            'product_items': [{ 
                'product_id': vindi_product_id,
                'pricing_schema': {
                    'price': price
                }
            }]
        }

        super(VindiSubscriptionSerializer, self).__init__(**kwargs)
        self.is_valid()


class VindiProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    status = serializers.CharField(default='active')
    description = serializers.CharField()
    pricing_schema = VindiPricingSchemaRelation()

    def __init__(self, product_name, product_description, price, *args, **kwargs):
        kwargs['data'] = {
            'name': product_name,
            'description': product_description,
            'pricing_schema': {
                'price': price,
            }
        }

        super(VindiProductSerializer, self).__init__(**kwargs)
        self.is_valid()