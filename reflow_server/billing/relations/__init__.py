from rest_framework import serializers

from reflow_server.billing.models import CompanyInvoiceMails


class CompanyInvoiceMailsRelation(serializers.ModelSerializer):
    class Meta:
        model = CompanyInvoiceMails
        fields = ('email',)
