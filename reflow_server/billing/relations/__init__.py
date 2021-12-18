from rest_framework import serializers

from reflow_server.billing.models import BillingPlanPermission, CompanyBilling, CompanyInvoiceMails


class TotalsByNameRelation(serializers.Serializer):
    name = serializers.CharField()
    total = serializers.CharField()
    quantity = serializers.IntegerField()

class CompanyInvoiceMailsRelation(serializers.ModelSerializer):
    email = serializers.CharField(error_messages={ 'null': 'blank', 'blank': 'blank' })
    
    class Meta:
        model = CompanyInvoiceMails
        fields = ('email',)


class PlanPermissionsRelation(serializers.ModelSerializer):
    class Meta:
        model = BillingPlanPermission
        fields = ('id', 'individual_charge_value_type_id','default_quantity', 'price_multiplicator',  'has_soft_limit')