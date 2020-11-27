from rest_framework import serializers

from reflow_server.rich_text.models import TextBlock, TextImageOption, TextListOption, \
    TextTextOption, TextTableOption, TextContent


class TableOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = TextTableOption
        fields = '__all__'


class TextOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = TextTextOption
        fields = '__all__'


class ListOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = TextListOption
        fields = '__all__'


class ImageOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = TextImageOption
        fields = '__all__'


class ContentRelation(serializers.ModelSerializer):
    order = serializers.IntegerField()
    uuid = serializers.UUIDField()
    text = serializers.CharField(allow_null=True, allow_blank=True)
    is_bold = serializers.BooleanField(default=False)
    is_italic = serializers.BooleanField(default=False)
    is_underline = serializers.BooleanField(default=False)
    is_code = serializers.BooleanField(default=False)
    latex_equation = serializers.CharField(allow_null=True, allow_blank=True)
    marker_color = serializers.CharField(allow_null=True, allow_blank=True)
    text_color = serializers.CharField(allow_null=True, allow_blank=True)
    link = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = TextContent
        fields = ('order', 'uuid', 'text', 'is_bold', 'is_italic', 'is_underline', 'is_code', 
                  'latex_equation', 'marker_color', 'text_color', 'link')


class BlockListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.parent.instance != None:
            data = data.filter(depends_on__isnull=True)
        return super(self.__class__, self).to_representation(data)


class BlockRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    uuid = serializers.UUIDField()
    image_option = ImageOptionRelation(allow_null=True)
    list_option = ListOptionRelation(allow_null=True)
    text_option = TextOptionRelation(allow_null=True)
    table_option = TableOptionRelation(allow_null=True)
    rich_text_block_contents = ContentRelation(many=True)

    # reference: https://stackoverflow.com/a/28947040
    def to_representation(self, data):
        #Add any self-referencing fields here (if not already done)
        self.fields['rich_text_depends_on_blocks'] = BlockRelation(data, many=True)      
        return super(BlockRelation, self).to_representation(data) 

    class Meta:
        model = TextBlock
        list_serializer_class = BlockListSerializer
        fields = ('id', 'uuid', 'image_option', 'list_option', 'text_option', 'table_option', 'block_type', 'order', 'rich_text_block_contents')
