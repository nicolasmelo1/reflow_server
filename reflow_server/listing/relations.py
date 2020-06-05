from rest_framework import serializers

from reflow_server.formulary.models import Field


class ListingHeaderFieldsRelation(serializer.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'label_name', 'name', 'type', 'user_selected')