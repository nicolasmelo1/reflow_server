from rest_framework import serializers
from rest_framework.fields import ListField

from reflow_server.authentication.models import Company, AddressHelper
from reflow_server.billing.services.data import CompanyChargeData
from reflow_server.billing.services import VindiService, BillingService, ChargeService
from reflow_server.billing.models import CompanyBilling, CurrentCompanyCharge, IndividualChargeValueType
from reflow_server.billing.relations import CompanyInvoiceMailsRelation, TotalsByNameRelation
from reflow_server.billing.utils import validate_cnpj, validate_cpf


class AddressOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressHelper
        fields = ('state', 'state_code', 'city')

class CurrentCompanyChargeListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        """
        This guarantees that all of the IndividualValueChargeType are in the response, so if we create a new one or anything like that, we guarantee
        it will appear for the user no matter if he had created it or not.
        """
        if isinstance(data.instance, Company):
            instance = CompanyBilling.objects.filter(company_id=data.instance.id).first()
            charge_service = ChargeService(data.instance.id, instance)
            current_company_charges = []
            current_company_charges_data = charge_service.validate_current_company_charges_and_create_new([])
            for current_company_charge in current_company_charges_data:
                current_company_charges.append(
                    CurrentCompanyCharge(
                        company_id=data.instance.id,
                        discount_by_individual_value=charge_service.get_discount_for_quantity(
                            current_company_charge.individual_value_charge_id,
                            current_company_charge.quantity
                        ),
                        individual_charge_value_type_id=current_company_charge.individual_value_charge_id,
                        quantity=current_company_charge.quantity
                    )
                )
            data = current_company_charges
        return super().to_representation(data)

    def create(self, validated_data):
        instance = CompanyBilling.objects.filter(company_id=self.context['company_id']).first()
        charge_service = ChargeService(self.context['company_id'], instance)
        current_company_charges = [
            CompanyChargeData(
                individual_value_charge_name=current_company_charge['individual_charge_value_type']['name'], 
                quantity=current_company_charge['quantity']
            ) 
            for current_company_charge in validated_data
        ]
        total_data = charge_service.get_total_data_from_custom_charge_quantity(current_company_charges)
        data = {
            'total': total_data.total,
            'discounts': total_data.total_coupons_discounts,
            'total_by_name': [{
                'name': key, 
                'quantity': value['quantity'],
                'total': value['value']
            } for key, value in total_data.total_by_charge_name.items()]
        }
        return data

class CurrentCompanyChargeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='individual_charge_value_type.name')
    quantity = serializers.IntegerField()

    class Meta:
        list_serializer_class = CurrentCompanyChargeListSerializer
        model = CurrentCompanyCharge
        fields = ('name', 'quantity')


class TotalsSerializer(serializers.Serializer):
    total = serializers.FloatField()
    discounts = serializers.FloatField()
    total_by_name = TotalsByNameRelation(many=True)


class CompanySerializer(serializers.ModelSerializer):
    company_invoice_emails = CompanyInvoiceMailsRelation(many=True)
    current_company_charges = CurrentCompanyChargeSerializer(many=True, error_messages={ 'null': 'blank', 'blank': 'blank' })

    class Meta:
        model = Company
        fields = ('company_invoice_emails', 'current_company_charges')
        
        
class PaymentSerializer(serializers.ModelSerializer):
    gateway_token = serializers.CharField(allow_null=True)
    company = CompanySerializer()
    payment_method_type_id = serializers.IntegerField(error_messages = { 'null': 'blank', 'blank': 'blank' })
    invoice_date_type_id = serializers.IntegerField(error_messages = { 'null': 'blank', 'blank': 'blank' })
    credit_card_data = serializers.SerializerMethodField(required=False)
    cnpj = serializers.CharField(error_messages={ 'null': 'blank', 'blank': 'blank' })
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
        vindi_service = VindiService(obj.company_id)
        return vindi_service.get_credit_card_info()

    def validate(self, data):
        self.billing_service = BillingService(self.instance.company_id)
        if not (validate_cnpj(data['cnpj']) or validate_cpf(data['cnpj'])):
            raise serializers.ValidationError(detail={'detail': 'cnpj', 'reason': 'invalid_registry_code'})
        if not self.billing_service.is_valid_company_invoice_emails(len(data['company']['company_invoice_emails'])):
            raise serializers.ValidationError(detail={'detail': 'company_invoice_emails', 'reason': 'cannot_be_bigger_than_three_or_less_than_one'})
        
        return data

    def update(self, instance, validated_data):
        current_company_charges = [
            CompanyChargeData(
                individual_value_charge_name=current_company_charge['individual_charge_value_type']['name'], 
                quantity=current_company_charge['quantity']
            ) 
            for current_company_charge in validated_data['company']['current_company_charges']
        ]
        emails = [company_invoice_email['email'] for company_invoice_email in validated_data['company']['company_invoice_emails']]

        self.billing_service.update_billing_information(
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
        model = CompanyBilling
        fields = ('gateway_token', 'company', 'payment_method_type_id', 'invoice_date_type_id', 
                  'credit_card_data', 'additional_details', 'cnpj', 'zip_code', 'street', 'state', 
                  'number', 'neighborhood', 'city', 'country') 
        