from rest_framework import serializers

from reflow_server.authentication.models import Company, AddressHelper
from reflow_server.billing.services import VindiService
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.billing.relations import CompanyInvoiceMailsRelation


class AddressOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressHelper
        fields = ('state', 'state_code', 'city')


class CurrentCompanyChargeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='individual_charge_value_type.name')
    quantity = serializers.IntegerField()
    user_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = CurrentCompanyCharge
        fields = ('name', 'quantity', 'user_id')


class PaymentSerializer(serializers.ModelSerializer):
    gateway_token = serializers.CharField(allow_null=True)
    cnpj = serializers.CharField(allow_null=True)
    company_invoice_emails = CompanyInvoiceMailsRelation(many=True)
    payment_method_type_id = serializers.IntegerField()
    invoice_date_type_id = serializers.IntegerField()
    address = serializers.CharField(allow_null=True, required=False)
    zip_code = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    street = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    state = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    number = serializers.IntegerField(allow_null=True, required=False)
    neighborhood = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    country = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    city = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    payment_data = serializers.SerializerMethodField(required=False)

    def get_payment_data(self, obj):
        vindi_service = VindiService(company_id=obj.id)
        return vindi_service.get_credit_card_info()

    class Meta:
        model = Company
        fields = ('gateway_token', 'company_invoice_emails', 'payment_method_type_id', 'invoice_date_type_id', 'cnpj', 'address', 'zip_code', 'street',
                  'state', 'number', 'neighborhood', 'country', 'city', 'payment_data') 