from rest_framework import serializers

from reflow_server.listing.models import ListingSelectedFields
from reflow_server.listing.relations import ListingHeaderFieldsRelation


class ListingHeaderListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

class ListingHeaderSerializer(serializers.ModelSerializer):
    field = ListingHeaderFieldsRelation()

    class Meta:
        model = ListingSelectedFields
        list_serializer_class = ListingHeaderListSerializer
        fields = ('id', 'field', 'is_selected')
