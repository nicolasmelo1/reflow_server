from rest_framework import serializers

from reflow_server.rich_text.models import TextPage, TextBlockTypeCanContainType
from reflow_server.rich_text.relations import BlockRelation


class PageSerializer(serializers.ModelSerializer):
    raw_text = serializers.CharField(allow_blank=True, allow_null=True)
    rich_text_page_blocks = BlockRelation(many=True)
    
    class Meta:
        model = TextPage
        fields = ('id', 'raw_text', 'rich_text_page_blocks')


class TextBlockTypeCanContainTypeSerializer(serializers.ModelSerializer):
    """
    This serializer holds the relation of all the block_types another block type (that has children blocks) 
    can contain.
    """
    class Meta:
        model = TextBlockTypeCanContainType
        fields = ('block_id', 'contain_id')