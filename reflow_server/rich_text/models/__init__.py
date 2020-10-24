from django.db import models


class TextBlockType(models.Model):
    name = models.CharField(max_length=250)
    is_primitive = models.BooleanField(default=False)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'text_block_type'
        ordering = ('order',)


class TextBlockTypeCanContainType(models.Model):
    block = models.ForeignKey('rich_text.TextBlockType', models.CASCADE, db_index=True, related_name='text_block_type_can_contain_block')
    contain = models.ForeignKey('rich_text.TextBlockType', models.CASCADE, db_index=True, related_name='text_block_type_can_contain')

    class Meta:
        db_table = 'text_block_type_can_contain_type'


class TextListType(models.Model):
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)
    
    class Meta:
        db_table = 'text_list_type'
        ordering = ('order',)


class TextAlignmentType(models.Model):
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'text_alignment_type'
        ordering = ('order',)


class TextPage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    raw_text = models.TextField(blank=True, null=True)
    markdown_text = models.TextField(blank=True, null=True)

    class Meta:
        db_table='text_page'


class TextTableOption(models.Model):
    rows_num = models.BigIntegerField(default=1)
    columns_num = models.BigIntegerField(default=1)
    border_color = models.CharField(max_length=150)

    class Meta:
        db_table = 'text_table_option'


class TextTextOption(models.Model):
    alignment_type = models.ForeignKey('rich_text.TextAlignmentType', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'text_text_option'


class TextListOption(models.Model):
    list_type = models.ForeignKey('rich_text.TextListType', models.CASCADE, db_index=True, null=False)
    
    class Meta:
        db_table = 'text_list_option'


class TextImageOption(models.Model):
    size_relative_to_view = models.BigIntegerField(default=100)
    
    class Meta:
        db_table = 'text_image_option'


class TextBlock(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    page = models.ForeignKey('rich_text.TextPage',  models.CASCADE, db_index=True, related_name='rich_text_page_blocks')
    image_option = models.ForeignKey('rich_text.TextImageOption', models.CASCADE, db_index=True, null=True)
    list_option = models.ForeignKey('rich_text.TextListOption', models.CASCADE, db_index=True, null=True)
    text_option = models.ForeignKey('rich_text.TextTextOption', models.CASCADE, db_index=True, null=True)
    table_option = models.ForeignKey('rich_text.TextTableOption', models.CASCADE, db_index=True, null=True)
    block_type = models.ForeignKey('rich_text.TextBlockType', models.CASCADE)
    order = models.BigIntegerField(default=1)
    depends_on = models.ForeignKey('self', models.CASCADE, db_index=True, null=True, related_name='rich_text_depends_on_blocks')

    class Meta:
        db_table='text_block'
        ordering=('order',)


class TextContent(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.BigIntegerField(default=1)
    block = models.ForeignKey('rich_text.TextBlock', models.CASCADE, db_index=True, related_name='rich_text_block_contents')
    text = models.TextField(blank=True, null=True)
    is_bold = models.BooleanField(default=False)
    is_italic = models.BooleanField(default=False)
    is_underline = models.BooleanField(default=False)
    is_code = models.BooleanField(default=False)
    latex_equation = models.TextField(null=True, blank=True)
    marker_color = models.CharField(max_length=150, null=True, blank=True)
    text_color = models.CharField(max_length=150, null=True, blank=True)
    link = models.TextField(blank=True, null=True)

    class Meta:
        db_table='text_content'
        ordering=('order',)