from rest_framework import serializers


class VindiClientAddressRelation(serializers.Serializer):
    street = serializers.CharField(allow_blank=True)
    number = serializers.CharField(allow_blank=True)
    zipcode = serializers.CharField(allow_blank=True)
    neighborhood = serializers.CharField(allow_blank=True)
    city = serializers.CharField(allow_blank=True)
    state = serializers.CharField(allow_blank=True)
    country = serializers.CharField(allow_blank=True)


class VindiClientMetadataRelation(serializers.Serializer):
    _cc_email = serializers.ListField(allow_empty=True)


class VindiPricingSchemaRelation(serializers.Serializer):
    price = serializers.FloatField()
    schema_type = serializers.CharField(default='flat')


class VindiSubscriptionProductItemRelation(serializers.Serializer):
    product_id = serializers.IntegerField()
    pricing_schema = VindiPricingSchemaRelation()

