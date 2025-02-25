from reflow_server.rich_text.models import TextBlockType, TextBlockTypeCanContainType
from reflow_server.rich_text.services.exceptions import RichTextValidationException

import inspect


class ContentData:
    def __init__(self, uuid, order, text, is_bold, is_italic, is_underline, is_code, 
                 is_custom, custom_value, latex_equation, marker_color, text_color, text_size, link):
        self.uuid = uuid
        self.order = order
        self.text = text
        self.is_bold = is_bold
        self.is_italic = is_italic
        self.is_underline = is_underline
        self.is_code = is_code
        self.is_custom = is_custom
        self.custom_value = custom_value
        self.latex_equation = latex_equation
        self.marker_color = marker_color
        self.text_color = text_color
        self.text_size = text_size
        self.link = link


class BlockData:
    def __init__(self, uuid, block_type_id, depends_on_uuid, order, block_type_id_name_reference):
        """
        This class will hold each block data, so all of the contents of a block, it's type, its uuid, the uuid it depends on and so on.
        The order is not defined when creating the BlockData using the `.add_block()` method in 'reflow_server.rich_text.services.data.PageData'
        instead we define the order when retrieving the list of blocks from the page.

        Args:
            uuid (uuid.UUID): The uuid of the block. This is more important than the actual id of the block. This uuid is created on the front-end 
                              and acts as the id of the block. With an uuid we can manage the id of the block in the front-end.
            block_type_id (int): The block_type id, is it a text, a table, what is this block?
            depends_on_uuid (int): If this block is dependent on another block you must set the uuid this block depends on. If it is not 
                                   dependant, just set this to None
            order (int): The order of the block, this way we can retrieve the blocks ordered.
            block_type_id_name_reference (dict): With this we can return the block_name using only the block_type_id.
        """
        self.uuid = uuid
        self.block_type_id = block_type_id
        self.depends_on_uuid = depends_on_uuid
        self.order = order
        self.contents = []
        self.__is_valid_cache = False
        self.__block_type_id_name_reference = block_type_id_name_reference

    def append_text_block_type_data(self, alignment_type_id):
        """
        If the block type is a text you need to append this extra data.

        Args:
            alignment_type_id (int): The id of the alignment type.
        """
        self.alignment_type_id = alignment_type_id

    def append_image_block_type_data(self, image_file_uuid, image_link='', image_file_name='', size_relative_to_view=1):
        """
        If the block type is of type `image`, you need to append this extra data.

        Args:
            image_link (str, optional): The link of the image, this is only needed if the image is from external source and not uploaded. Defaults to ''.
            image_file_name (str, optional): The name of the file, can be a draft so we need to always check if it is or not a draft. Defaults to ''.
            size_relative_to_view (int, optional): This is the size multiplied by the width of the view. Defaults to 1.
        """
        self.image_file_uuid = image_file_uuid
        self.image_link = image_link
        self.image_file_name = image_file_name
        self.size_relative_to_view = size_relative_to_view

    def append_table_block_type_data(self, border_color, column_dimensions, row_dimensions):
        """
        If the block type is of type `table`, you need to append this extra data.

        Args:
            border_color (str): The color of the border of the table
            column_dimensions (list({'width': int}) || list(int)): The list of the dimensions as % for each column.
            row_dimensions (list({'height': int}) || list(int)): The list of the dimensions as px for each row.
        """
        self.border_color = border_color
        self.column_dimensions = [column_dimension if str(column_dimension).isdigit() else column_dimension['width'] for column_dimension in column_dimensions]
        self.row_dimensions = [row_dimension if str(row_dimension).isdigit() else row_dimension['height'] for row_dimension in row_dimensions]

    def __validate_block_type_data(self):
        """
        This validates if the block has the data needed BEFORE adding the contents. This validates also the block types. 
        If the block requests more data then the ones defined in the constructor of this class we return an error.

        Raises:
            ValueError: If the type of the block needs some more data, than the data passed in the constructor returns an
            error.
        """
        if self.__is_valid_cache:
            return
        else:
            block_name = self.__block_type_id_name_reference[self.block_type_id]
            method_name = 'append_%s_block_type_data' % block_name
            handler = getattr(self, method_name, None)
            # For reference on what i'm doing here https://stackoverflow.com/a/582193
            for key in list(inspect.signature(handler).parameters):
                if not hasattr(self, key):
                    raise RichTextValidationException('For block of type `{}` you must set additional values using `.{}()` method.'.format(block_name, method_name))
            self.__is_valid_cache = True

    def add_content(self, uuid, text, is_bold, is_italic, is_underline, is_code, 
                    is_custom, custom_value, latex_equation, marker_color, text_color, 
                    text_size, link):
        """
        Adds each content of the block. A content is an inline content. If the text is Bold, Italic, Underlined and so on you define it here. 
        The content is each inline configuration.

        Args:
            uuid (uuid.UUID): The uuid of the content, each content has a unique uuid so we can distinguish between them
            text (str): The string of the content, since it is inline this holds the text that should be rendered.
            is_bold (bool): Is the content bold
            is_italic (bool): is the content italic
            is_underline (bool): is the content underlined
            is_code (bool): is the content a code (code adds a simple grey background)
            is_custom (bool): if the content custom (custom contents are not handled by the rich text itself it is used so that
                              you can create custom contents in other places. On PDF for example, a custom would be a field id 
                              to use as parameter)
            custom_value (str): If the content is custom this custom_value is used so you can know what to render on this content
                                in the front end
            latex_equation (str): Not used right now but we will support latex equations in the future so you can write your classes and papers
                                  inside of reflow
            marker_color (str): The color of the background of this content
            text_color (str): The hex color of the text of this content
            text_size (int): The size of the Text.
            link (str): If your text is a link you set the link here.

        Returns:
            reflow_server.rich_text.data.ContentData: Returns a content object, you actually don't need to use this object for anything except when
                                                      saving the rich_text data.
        """
        self.__validate_block_type_data()
        order = len(self.contents)
        content_data = ContentData(uuid, order, text, is_bold, is_italic, is_underline, is_code, 
                                   is_custom, custom_value, latex_equation, marker_color, text_color, 
                                   text_size, link)
        self.contents.append(content_data)
        return content_data
    
    @property
    def block_name(self):
        return self.__block_type_id_name_reference[self.block_type_id]


class PageData:
    def __init__(self, page_id=None, allowed_blocks=[]):
        """
        This page data is what we use to handle the rich text data. We do not handle with serializers directly. Like formulary data
        we convert first everything to this python object so we can handle better in the services.
        With this class 
        - You first need to create a new object defining the `page_id`, this will expose a function to add blocks: `.add_block()`.
        - When you add a new block using the `.add_block()` block function it returns a BlockData object.
        - The BlockData object will expose the `.add_content()` function so you can add each content.
        - IMPORTANT: For some block types you need to append extra data. You can use `.append_<block_type_name>_type_data()` methods

        Use `.blocks` to return a list of blocks.

        The `.add_block` function automatically ads the blocks in order. Just make sure that you add the dependent blocks AFTER you add the block
        it depends on.

        Args:
            page_id (int, optional): If you are editing a page, you should set this variable. Defaults to None.
        """
        self.page_id = page_id
        self.__allowed_block_ids = allowed_blocks
        self.__blocks = []
        self.__block_can_contain_blocks = {}
        self.block_type_id_name_reference = {text_block_type.id: text_block_type.name for text_block_type in TextBlockType.rich_text_.all_block_types()}
        self.__depends_on_block_reference = {}
        self.__block_uuid_types = {}
        self.__depends_on_sum_reference = {}

        for block_type_can_contain_type in TextBlockTypeCanContainType.rich_text_.all_block_type_can_contain_types():
            self.__block_can_contain_blocks[block_type_can_contain_type.block_id] = self.__block_can_contain_blocks.get(
                block_type_can_contain_type.block_id, []
            ) + [block_type_can_contain_type.contain_id]

    def add_block(self, uuid, block_type_id, depends_on_uuid=None):
        """
        This automagically ads everything in order. When a new block arrives we check if it is dependent, if it is we find the index of
        the uuid it depends on in the list. If the id it depends on was not inserted it raises an error telling you to add the block in 
        order.
        It makes other 2 validations besides that: 
        - We check if this block type is allowed to be saved in this current context (like for PDF_generator we might not want
        some blocks to be valid)
        - We check if the block type can contain a block type. We validate through the hole nesting, so in a case where a table is valid inside
        a listing, and a listing inside of a table. If the user creates a table, and inside the table creates a listing and adds another table
        we prevent this from happening, the user will ONLY be able to insert inside of the listing in the table block that is common for both
        the listing and the table.

        So, you first need to add non-dependant blocks and AFTER you add the dependant blocks.
    
        Args:
            uuid (uuid.UUID): The uuid of the block. This is more important than the actual id of the block. This uuid is created on the front-end.
            block_type_id (int): The block_type id, is it a text, a table, what is this block?
            depends_on_uuid (int, optional): If this block is dependent on another block you must set the uuid this block depends on. 
                                             Defaults to None.

        Raises:
            AssertionError: If you add a dependent block BEFORE adding the block it depends on it raises an error. To make it easier for users.
            you can use the `.ordered_list_from_serializer_data_for_page_data()` function in reflow_server.rich_text.services.utils to convert the
            data from your serializer so you can easily insert it here.

        Returns:
            reflow_server.rich_text.services.data.BlockData: The block object that exposes the `.add_content()` method.
        """
        self.__block_uuid_types[uuid] = block_type_id
        if self.__allowed_block_ids and block_type_id not in self.__allowed_block_ids:
            raise RichTextValidationException('The block id `{}` is not a valid block. Please use one of the following: {}'.format(
                str(block_type_id), 
                ', '.join([str(allowed_block_id) for allowed_block_id in self.__allowed_block_ids])
            ))
        if depends_on_uuid:
            self.__depends_on_block_reference[uuid] = depends_on_uuid
            index_to_insert_block = None
            for index, block in enumerate(self.__blocks):
                if str(depends_on_uuid) == str(block.uuid):
                    index_to_insert_block = index + self.__depends_on_sum_reference.get(str(depends_on_uuid), 1)
                    self.__depends_on_sum_reference[str(depends_on_uuid)] = self.__depends_on_sum_reference.get(str(depends_on_uuid), 1) + 1
                    break
            if index_to_insert_block == None:
                raise RichTextValidationException('You must add block with uuid `{}`, before the block with uuid `{}`'.format(depends_on_uuid, uuid))
            parent_block_uuid = depends_on_uuid
            parent_block_can_have_block_types = self.__block_can_contain_blocks[self.__block_uuid_types[parent_block_uuid]]
            while parent_block_uuid:
                parent_block_uuid = self.__depends_on_block_reference.get(depends_on_uuid, None)
                if parent_block_uuid:
                    parent_block_can_have_block_types = [parent_block_can_have_type for parent_block_can_have_type in parent_block_can_have_block_types 
                                                        if parent_block_can_have_type in self.__block_can_contain_blocks[self.__block_uuid_types[parent_block_uuid]]]
                if block_type_id not in parent_block_can_have_block_types:
                    raise RichTextValidationException('Non valid block_type id `{}` inside of block uuid `{}`'.format(str(block_type_id), str(depends_on_uuid)))

        else:
            index_to_insert_block = len(self.__blocks)
        
        block_data = BlockData(uuid, block_type_id, str(depends_on_uuid), None, self.block_type_id_name_reference)
        self.blocks.insert(index_to_insert_block, block_data)
        return block_data

    @property
    def blocks(self):
        """
        Returns the blocks and also adds the order to each block, use this to retrieve the list of blocks.
        """
        for index, block in enumerate(self.__blocks):
            block.order = index
        return self.__blocks
