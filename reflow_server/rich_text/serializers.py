from rest_framework import serializers

from reflow_server.rich_text.models import TextPage
from reflow_server.rich_text.relations import BlockRelation
from reflow_server.rich_text.services.data import PageData
from reflow_server.rich_text.services import RichTextService
from reflow_server.rich_text.services import ordered_list_from_serializer_data_for_page_data

class PageSerializer(serializers.ModelSerializer):
    raw_text = serializers.CharField(allow_blank=True, allow_null=True)
    rich_text_page_blocks = BlockRelation(many=True)
    
    class Meta:
        model = TextPage
        fields = ('id', 'raw_text', 'rich_text_page_blocks')
