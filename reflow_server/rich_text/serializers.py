from rest_framework import serializers

from reflow_server.rich_text.models import TextPage
from reflow_server.rich_text.relations import BlockRelation


class PageSerializer(serializers.ModelSerializer):
    raw_text = serializers.CharField()
    rich_text_page_blocks = BlockRelation(many=True)
    
    class Meta:
        model = TextPage
        fields = ('id', 'raw_text', 'rich_text_page_blocks')