from rest_framework import serializers

from reflow_server.billing.models import CompanyInvoiceMails


class CompanyInvoiceMailsRelation(serializers.ModelSerializer):
    email = serializers.CharField(error_messages={ 'null': 'blank', 'blank': 'blank' })
    
    class Meta:
        model = CompanyInvoiceMails
        fields = ('email',)
