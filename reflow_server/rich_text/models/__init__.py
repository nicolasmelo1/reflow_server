from django.conf import settings
from django.db import models

from reflow_server.rich_text.managers import RichTextTextBlockTypeManager, RichTextTextImageOptionManager, \
    RichTextTextBlockManager, RichTextTextContentManager, RichTextTextTableOptionManager, \
    RichTextTextTableOptionColumnDimensionManager, RichTextTextTableOptionRowDimensionManager
from reflow_server.pdf_generator.managers import TextPagePDFGeneratorManager

import uuid

# TODO: Documentation here
class TextBlockType(models.Model):
    name = models.CharField(max_length=250)
    is_primitive = models.BooleanField(default=False)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'text_block_type'
        ordering = ('order',)

    rich_text_ = RichTextTextBlockTypeManager()
    objects = models.Manager()
    

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
    """
    The page is the common ancestor for every block and content. A Page represents literally a hole note page. If you want to bound a rich text data
    to anything, you will probably might want to bound to this. A page is made up by blocks and each block by contents.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True, null=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True, null=True)
    raw_text = models.TextField(blank=True, null=True)
    markdown_text = models.TextField(blank=True, null=True)

    class Meta:
        db_table='text_page'

    objects = models.Manager()
    pdf_generator_ = TextPagePDFGeneratorManager()


class TextTableOptionRowDimension(models.Model):
    """
    This holds the height as px for each row in our table. Since this holds the height for EACH row this also holds the
    number of rows of a table.

    Each row is bounded to a `text_table_option` since this only for `table` blocks
    """
    height = models.BigIntegerField(default=None, null=True)
    text_table_option = models.ForeignKey('rich_text.TextTableOption', models.CASCADE, db_index=True, related_name='text_table_option_row_dimensions')
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'text_table_option_row_dimension'
        ordering = ('order',)

    rich_text_ = RichTextTextTableOptionRowDimensionManager()


class TextTableOptionColumnDimension(models.Model):
    """
    This holds the width as % for each column in our table. Since this holds the width for EACH column this also holds the
    number of columns of a table.

    Each column is bounded to a `text_table_option` since this only for `table` blocks
    """
    width = models.BigIntegerField(default=None, null=True)
    text_table_option = models.ForeignKey('rich_text.TextTableOption', models.CASCADE, db_index=True, related_name='text_table_option_column_dimensions')
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'text_table_option_column_dimension'
        ordering = ('order',)

    rich_text_ = RichTextTextTableOptionColumnDimensionManager()


class TextTableOption(models.Model):
    """
    When saving table blocks we handle it a little bit differently from other block types, but not so much.
    First things first: a table block is a block that has children blocks, differently from `text` and `image`
    the `table` block type does not live by itself, it uses children blocks on its contents. To understand more about
    children blocks read more on `TextBlock` to understand the recurssiveness of the blocks.

    Okay, so how does this data here helps us creating table blocks? So this model as you can see is really simple, it just
    saves the border_color. But we have auxiliary tables that are bounded to this model: TextTableOptionColumnDimension 
    and TextTableOptionRowDimension. The first one holds the width as % of each column of the table, and since we hold 
    the width of EACH column, counting it we have the number of columns of the table. Now to the second one TextTableOptionRowDimension,
    as you might have guessed, this holds the height of each row, but here it's units are pixels. Same as the column one,
    if you count this model you will have the number of rows of a table.
    """
    border_color = models.CharField(max_length=150, null=True, blank=True)
    
    class Meta:
        db_table = 'text_table_option'

    rich_text_ = RichTextTextTableOptionManager()


class TextTextOption(models.Model):
    alignment_type = models.ForeignKey('rich_text.TextAlignmentType', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'text_text_option'


class TextListOption(models.Model):
    list_type = models.ForeignKey('rich_text.TextListType', models.CASCADE, db_index=True, null=False)
    
    class Meta:
        db_table = 'text_list_option'


class TextImageOption(models.Model):
    """
    Those are the options for `image` block type specifically. If your block is an image you can use those options.
    Be aware that `bucket`, `file_image_path` and even `file_url` should NEVER be sent to the front-end.

    Images can be from sources like google images, or other urls and also from the user computer. If the file is from the
    computer of a user, it should be private, so no one outside reflow should be able to see it. Otherwise it's a public
    url so no need to protect it.

    The `size_relative_to_view` can be 1 or 0, we multiply it by the percentage of the width of the page.

    The `file_image_uuid` is a unique id for each image. This way, when saving, if another block is using an uuid that already exists
    we can just duplicate the image of this block instead of saving a new file. This make easier for us to duplicate blocks inside of
    the rich text. Specially the ones that already exists. If we did not made this on the front-end we would need to download the file
    from the url and then reupload it when saving. It is kinda a hacky and a clumbersome way to do this. 
    Using `file_image_uuid` it becomes a lot easier for us to duplicate
    """
    size_relative_to_view = models.DecimalField(default=1.00, max_digits=25, decimal_places=20)
    link = models.TextField(default=None, blank=True, null=True)
    bucket = models.CharField(max_length=200, default=settings.S3_BUCKET, blank=True, null=True)
    file_image_uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    file_image_path = models.CharField(max_length=250, default=settings.S3_FILE_RICH_TEXT_IMAGE_PATH, blank=True, null=True)
    file_url = models.CharField(max_length=1000, null=True, blank=True)
    file_size = models.BigIntegerField(default=0, blank=True, null=True)
    file_name = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'text_image_option'

    rich_text_ = RichTextTextImageOptionManager()
    

class TextBlock(models.Model):
    """
    The rich text works similar to Notion.so and Coda.io. We use the idea that everything is separated by blocks. Google Docs and Word are outside of the scope
    on what this rich text is supposed to do. This should be more a Notes editor than a page and documents editor.

    Making stuff this way we have more control over data, we can extend it more than a normal text can. We can create N types of blocks, from fetching data
    from a page internally, to iframing contents inside of the block. Remember that: every block type that you create WILL BE available for ALL THE RICH TEXTS.

    IMPORTANT: Blocks are recursive, this means you can have Block inside of a block and so on, for that you use the depends_on.
    This is important because on tables for example we might want to use the text block funcionality on each cell. On list block type each bullet point will
    be a text block.

    Each block can be of custom types also, similarly like TextContent but we do not support it yet. 
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
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

    objects = models.Manager()
    rich_text_ = RichTextTextBlockManager()
    

class TextContent(models.Model):
    """
    This holds every content of a text, it is usually bound to a block. A content is basically the text of the text block.
    When the user is typing a rich text, parts of the text can be bold, italic, underlined and so on. Each part of the text is a content.
    If a text is underlined it is a content, if the text is bold, it is a content. With this we can know the state for each part of the 
    text.

    Right now the text can be bold, italic, underlined, code or custom (this one is special). Other states includes the background color, the text color
    the size of the text, a link and so on.

    ABOUT CUSTOM:
    `is_custom` and `custom_value` are special cases here. They are contents that are handled by the domain that's using the rich text. What it means is that
    we can have many types of custom values in the rich text. For a PDF templates for example we want to display the field variable in the middle of the text,
    this is something managed entirely by the PDF Generator domain, and is not handled here. For other use cases for example we might want to tag users, tag
    pages, and so on. That is why we use the custom. How the custom value is rendered in the page, is also handled in the domain. 
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(default=uuid.uuid4, db_index=True)
    order = models.BigIntegerField(default=1)
    block = models.ForeignKey('rich_text.TextBlock', models.CASCADE, db_index=True, related_name='rich_text_block_contents')
    text = models.TextField(blank=True, null=True)
    is_bold = models.BooleanField(default=False)
    is_italic = models.BooleanField(default=False)
    is_underline = models.BooleanField(default=False)
    is_code = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=False)
    custom_value = models.TextField(blank=True, null=True, default=None)
    latex_equation = models.TextField(null=True, blank=True, default=None)
    marker_color = models.CharField(max_length=150, null=True, blank=True, default='')
    text_color = models.CharField(max_length=150, null=True, blank=True, default='')
    text_size = models.IntegerField(default=12)
    link = models.TextField(blank=True, null=True, default='')

    class Meta:
        db_table='text_content'
        ordering=('order',)

    objects = models.Manager()
    rich_text_ = RichTextTextContentManager()