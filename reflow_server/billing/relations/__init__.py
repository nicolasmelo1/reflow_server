from rest_framework import serializers

from reflow_server.billing.models import CompanyInvoiceMails


class TotalsByNameRelation(serializers.Serializer):
    name = serializers.CharField()
    total = serializers.CharField()
    quantity = serializers.IntegerField()

class CompanyInvoiceMailsRelation(serializers.ModelSerializer):
    email = serializers.CharField(error_messages={ 'null': 'blank', 'blank': 'blank' })
    
    class Meta:
        model = CompanyInvoiceMails
        fields = ('email',)
