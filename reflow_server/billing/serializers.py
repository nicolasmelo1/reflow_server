from rest_framework import serializers

from reflow_server.billing.relations import VindiClientAddressRelation, VindiClientMetadataRelation


class VindiClientSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()
    address = VindiClientAddressRelation()
    registry_code = serializers.CharField(allow_null=True)
    metadata = VindiClientMetadataRelation()

    