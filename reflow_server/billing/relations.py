from rest_framework import serializers


class VindiClientAddressRelation(serializers.Serializer):
    street = serializers.CharField(allow_blank=True)
    number = serializers.CharField(allow_blank=True)
    zipcode = serializers.CharField(allow_blanK=True)
    neighborhood = serializers.CharField(allow_blanK=True)
    cirty = serializers.CharField(allow_blanK=True)
    state = serializers.CharField(allow_blanK=True)
    country = serializers.CharField(allow_blanK=True)


class VindiClientMetadataRelation(serializers.Serializer):
    _cc_email = serializers.ListField(allow_empty=True)