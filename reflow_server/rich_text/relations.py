from rest_framework import serializers

from reflow_server.rich_text.models import TextBlock, TextImageOption, TextListOption, \
    TextTextOption, TextTableOption, TextContent, TextTableOptionRowDimension, TextTableOptionColumnDimension


class TableOptionRowDimension(serializers.ModelSerializer):
    height = serializers.IntegerField(allow_null=True)

    class Meta:
        model = TextTableOptionRowDimension
        fields = ('height',)


class TableOptionColumnDimension(serializers.ModelSerializer):
    width = serializers.FloatField(allow_null=True)

    class Meta:
        model = TextTableOptionColumnDimension
        fields = ('width',)


class TableOptionRelation(serializers.ModelSerializer):
    border_color = serializers.CharField(allow_null=True, allow_blank=True)
    text_table_option_row_dimensions = TableOptionRowDimension(many=True)
    text_table_option_column_dimensions = TableOptionColumnDimension(many=True)

    class Meta:
        model = TextTableOption
        fields = ('id', 'border_color', 'text_table_option_row_dimensions', 'text_table_option_column_dimensions')


class TextOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = TextTextOption
        fields = '__all__'


class ListOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = TextListOption
        fields = '__all__'


class ImageOptionRelation(serializers.ModelSerializer):
    link = serializers.CharField(allow_null=True, allow_blank=True)
    file_name = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = TextImageOption
        fields = ('id', 'size_relative_to_view', 'file_image_uuid', 'link', 'file_name')


class ContentRelation(serializers.ModelSerializer):
    order = serializers.IntegerField()
    uuid = serializers.UUIDField()
    text = serializers.CharField(allow_null=True, allow_blank=True)
    is_bold = serializers.BooleanField(default=False)
    is_italic = serializers.BooleanField(default=False)
    is_underline = serializers.BooleanField(default=False)
    is_code = serializers.BooleanField(default=False)
    is_custom = serializers.BooleanField(default=False)
    custom_value = serializers.CharField(allow_null=True, allow_blank=True)
    latex_equation = serializers.CharField(allow_null=True, allow_blank=True)
    marker_color = serializers.CharField(allow_null=True, allow_blank=True)
    text_color = serializers.CharField(allow_null=True, allow_blank=True)
    link = serializers.CharField(allow_null=True, allow_blank=True)

    class Meta:
        model = TextContent
        fields = ('order', 'uuid', 'text', 'is_bold', 'is_italic', 'is_underline', 'is_code', 
                  'is_custom', 'custom_value', 'latex_equation', 'marker_color', 'text_color', 
                  'link')


class BlockListSerializer(serializers.ListSerializer):
    def __init__(self, *args, **kwargs): 
        super(BlockListSerializer, self).__init__(*args, **kwargs)
    
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

    # this is for handling when the serializer recieves a data.
    def to_internal_value(self, data):
        if data.get('rich_text_depends_on_blocks', []):
            self.fields['rich_text_depends_on_blocks'] = BlockRelation(data, many=True)      
        return super(BlockRelation, self).to_internal_value(data) 

    # reference: https://stackoverflow.com/a/28947040
    # this is for handling when the data is being served
    def to_representation(self, data):
        #Add any self-referencing fields here (if not already done)
        self.fields['rich_text_depends_on_blocks'] = BlockRelation(data, many=True)      
        return super(BlockRelation, self).to_representation(data) 

    class Meta:
        model = TextBlock
        list_serializer_class = BlockListSerializer
        fields = ('id', 'uuid', 'image_option', 'list_option', 'text_option', 'table_option', 'block_type', 'order', 'rich_text_block_contents')
