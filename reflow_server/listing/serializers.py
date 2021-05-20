from rest_framework import serializers

from reflow_server.listing.models import ListingSelectedFields
from reflow_server.listing.relations import ListingHeaderFieldsRelation


class ListingHeaderSerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving the headers of listing visualization.
    """
    id = serializers.IntegerField(required=False, allow_null=True)
    field = ListingHeaderFieldsRelation()

    def create(self, validated_data):
        instance, _ = ListingSelectedFields.objects.update_or_create(
            id=validated_data.get('id', None),
            defaults={
                'field_id': validated_data['field']['id'],
                'is_selected': validated_data['is_selected'],
                'user_id': self.context['user_id']
            }
        )
        return instance
        
    class Meta:
        model = ListingSelectedFields
        fields = ('id', 'field', 'is_selected')
