from rest_framework import serializers

from reflow_server.authentication.models import Company, AddressHelper
from reflow_server.billing.services.data import CompanyChargeData
from reflow_server.billing.services import VindiService, BillingService
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.billing.relations import CompanyInvoiceMailsRelation
from reflow_server.billing.utils import validate_cnpj, validate_cpf

class AddressOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressHelper
        fields = ('state', 'state_code', 'city')


class CurrentCompanyChargeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='individual_charge_value_type.name')
    quantity = serializers.IntegerField()
    user_id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = CurrentCompanyCharge
        fields = ('name', 'quantity', 'user_id')


class TotalsSerializer(serializers.Serializer):
    name = serializers.CharField()
    total = serializers.CharField()


class PaymentSerializer(serializers.ModelSerializer):
    gateway_token = serializers.CharField(allow_null=True)
    company_invoice_emails = CompanyInvoiceMailsRelation(many=True)
    payment_method_type_id = serializers.IntegerField(error_messages = { 'null': 'blank', 'blank': 'blank' })
    invoice_date_type_id = serializers.IntegerField(error_messages = { 'null': 'blank', 'blank': 'blank' })
    credit_card_data = serializers.SerializerMethodField(required=False)
    current_company_charges = CurrentCompanyChargeSerializer(many=True, error_messages = { 'null': 'blank', 'blank': 'blank' })
    cnpj = serializers.CharField(error_messages = { 'null': 'blank', 'blank': 'blank' })
    zip_code = serializers.CharField(error_messages = { 'null': 'blank', 'blank': 'blank' })
    additional_details = serializers.CharField(allow_null=True, required=False)
    zip_code = serializers.CharField(
        error_messages = {'null': 'blank', 'blank': 'blank', 'min_length': 'invalid', 'max_length': 'invalid'}, 
        min_length=8, max_length=8
    )
    street = serializers.CharField(error_messages = { 'null': 'blank', 'blank': 'blank'})
    state = serializers.CharField(error_messages = { 'null': 'blank', 'blank': 'blank'})
    number = serializers.IntegerField(error_messages = { 'null': 'blank', 'blank': 'blank'})
    country = serializers.CharField(allow_null=True)
    neighborhood = serializers.CharField(error_messages = { 'null': 'blank', 'blank': 'blank'})
    city = serializers.CharField(error_messages = { 'null': 'blank', 'blank': 'blank'})

    def get_credit_card_data(self, obj):
        vindi_service = VindiService(company_id=obj.id)
        return vindi_service.get_credit_card_info()

    def validate(self, data):
        if not (validate_cnpj(data['cnpj']) or validate_cpf(data['cnpj'])):
            raise serializers.ValidationError(detail={'detail': 'cnpj', 'reason': 'invalid_registry_code'})
        return data

    def update(self, instance, validated_data):
        current_company_charges = [
            CompanyChargeData(
                individual_value_charge_name=current_company_charge['individual_charge_value_type']['name'], 
                quantity=current_company_charge['quantity'], 
                user_id=current_company_charge['user_id']
            ) 
            for current_company_charge in validated_data['current_company_charges']
        ]
        emails = [company_invoice_email['email'] for company_invoice_email in validated_data['company_invoice_emails']]

        billind_service = BillingService.update_billing(
            instance.id, 
            payment_method_type_id=validated_data['payment_method_type_id'],
            invoice_date_type_id=validated_data['invoice_date_type_id'],
            emails=emails,
            current_company_charges=current_company_charges,
            cnpj=validated_data['cnpj'],
            zip_code=validated_data['zip_code'],
            street=validated_data['street'],
            state=validated_data['state'], 
            number=validated_data['number'], 
            neighborhood=validated_data['neighborhood'], 
            country=validated_data.get('country', None), 
            city=validated_data['city'], 
            additional_details=validated_data.get('additional_details', None),
            gateway_token=validated_data.get('gateway_token', None)
        )
        
        return instance

    class Meta:
        model = Company
        fields = ('gateway_token', 'company_invoice_emails', 'payment_method_type_id', 
                  'current_company_charges', 'invoice_date_type_id', 'credit_card_data',
                  'additional_details', 'cnpj', 'zip_code', 'street', 'state', 'number', 
                  'neighborhood', 'city', 'country') 
        