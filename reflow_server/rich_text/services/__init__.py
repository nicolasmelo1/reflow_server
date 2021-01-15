from django.db import transaction

from reflow_server.rich_text.services.data import PageData
from reflow_server.rich_text.services.utils import ordered_list_from_serializer_data_for_page_data
from reflow_server.rich_text.services.block import RichTextImageBlockService
from reflow_server.rich_text.models import TextContent, TextPage, TextBlock, TextTextOption


class RichTextBlockException(NotImplementedError):
    pass


class RichTextService:
    def __init__(self, company_id, user_id):
        self.company_id = company_id
        self.user_id = user_id

    def _image_block_will_be_removed_handler(self, page_id, block):
        """
        Handles the deletion of `image` block types. This is needed because we need to remove the file 
        from our storage service

        Args:
            page_id (int): The id of the page that is being removed.
            block (reflow_server.rich_text.models.TextBlock): A rich text block instance that will be removed

        Returns:
            bool: returns True indicating everything went fine
        """
        rich_text_image_block_service = RichTextImageBlockService(page_id, self.user_id, self.company_id)
        rich_text_image_block_service.remove_image_block(block)
        return True
    
    def __block_will_be_removed_handler(self, page_id, block):
        handler = getattr(self, '_%s_block_will_be_removed_handler' % block.block_type.name, None)
        if handler:
            handler(page_id, block)
        return block

    def __remove_old_blocks_and_contents(self, page_instance, block_instances, content_instances):
        """
        Removes the blocks and contents that were removed from the rich_text. It's important to notice that we 
        loop through each block that will be removed so we can handle special use cases like delete files and such.

        Args:
            page_instance (reflow_server.rich_text.models.TextPage): The saved text_page instance we use this to filter the blocks from this page.
            block_instances (list(reflow_server.rich_text.models.TextBlock)): The saved block instances, we use this to exclude all of the saved block 
            instances from the filter so we can delete the one's from the page but not on this list.
            content_instances (list(reflow_server.rich_text.models.TextContent)): Same as the block_instances but instead we filter from the block_instances
            and removes the content_instances from the filter, this way we can remove the contents that were removed from the database.

        Returns:
            bool: returns True to indicate everything was deleted.
        """
        if block_instances:
            will_be_removed_blocks = TextBlock.rich_text_.text_blocks_by_page_id_excluding_block_ids(page_instance.id, [block_instance.id for block_instance in block_instances])
        else:
            will_be_removed_blocks = TextBlock.rich_text_.text_blocks_by_page_id(page_id=page_instance.id)
        
        if will_be_removed_blocks:
            for block in will_be_removed_blocks:
                self.__block_will_be_removed_handler(page_instance.id, block)
            will_be_removed_blocks.delete()

        if content_instances:
            will_be_removed_contents = TextContent.rich_text_.text_contents_by_page_id_excluding_content_ids(page_instance.id, [content_instance.id for content_instance in content_instances])
        else: 
            will_be_removed_contents = TextContent.rich_text_.text_contents_by_page_id(page_instance.id)
        
        if will_be_removed_contents:
            will_be_removed_contents.delete()
        return True

    @transaction.atomic
    def save_rich_text(self, page_data):
        """
        Method for saving the rich text page data in the database. Obviously first we create a page. Then we save each block (luckly we use
        the PageData object so all of the blocks are already ordered for us) and after saving each block we save each content of the block.
        We add each block to dict where each UUID is the key and each TextBlock instance is the value. This way we can reference the blocks
        the block depends on.

        After saving all blocks and contents we remove the older blocks and the older contents. That was removed.

        Args:
            page_data (reflow_server.rich_text.services.data.PageData): This object is responsible for holding all of the data of the page. 
                                                                        It's blocks each block content. You can read more about it in the 
                                                                        class constructor.

        Returns:
            reflow_server.rich_text.models.TextPage: The updated or created TextPage instance.
        """
        page_instance, __ = TextPage.objects.update_or_create(
            id=page_data.page_id,
            defaults={
                'company_id': self.company_id,
                'user_id': self.user_id,
                'raw_text': '',
                'markdown_text': ''
            }
        )

        saved_uuids_contents_reference = {}
        saved_uuids_blocks_reference = {}
        for block in page_data.blocks:
            block_instance, __ = TextBlock.objects.update_or_create(
                page_id=page_instance.id,
                uuid=block.uuid,
                defaults={
                    'order': block.order,
                    'block_type_id': block.block_type_id,
                    'depends_on': saved_uuids_blocks_reference.get(block.depends_on_uuid, None)
                }
            )
            self._save_block_types(block_instance, block)
            saved_uuids_blocks_reference[str(block.uuid)] = block_instance

            for content in block.contents:
                content_instance, __ = TextContent.objects.update_or_create(
                    block_id=block_instance.id,
                    uuid=content.uuid,
                    defaults={
                        'order': content.order,
                        'text': content.text,
                        'is_bold': content.is_bold,
                        'is_italic': content.is_italic,
                        'is_underline': content.is_underline,
                        'is_code': content.is_code,
                        'is_custom': content.is_custom,
                        'custom_value': content.custom_value,
                        'latex_equation': content.latex_equation,
                        'marker_color': content.marker_color,
                        'text_color': content.text_color,
                        'text_size': content.text_size,
                        'link': content.link,
                    }
                )
                saved_uuids_contents_reference[str(content.uuid)] = content_instance

        self.__remove_old_blocks_and_contents(
            page_instance, 
            saved_uuids_blocks_reference.values(), 
            saved_uuids_contents_reference.values()
        )
        return page_instance
    
    def _save_block_types(self, block_instance, block_data):
        """
        Some blocks have custom data. We use this to save this custom data to the block. In case of `text` blocks for example
        we need to add the alignment_type_id, for this we use the TextTextOption model and then bound this TextTextOption instance to the 
        `block_instance`.

        Args:
            block_instance (reflow_server.rich_text.models.TextBlock): The model instance of the updated or created block
            block_data (reflow_server.rich_text.services.data.BlockData): This object holds the data of the block that will be used
                                                                          for saving in the database.
        """
        handler = getattr(self, '_save_%s_block_type' % block_data.block_name, None)
        if handler:
            handler(block_instance, block_data)
        else:
            raise RichTextBlockException(
                'We cannot handle to save this type of block, '
                'make sure a `._save_<YourBlockTypeName>_block_type()` method exists in this class'
            )

    def _save_text_block_type(self, block_instance, block_data):
        text_option_instance, __ = TextTextOption.objects.update_or_create(
            id=block_instance.text_option.id if block_instance.text_option else None,
            defaults={
                'alignment_type': block_data.alignment_type_id
            }
        )
        block_instance.text_option = text_option_instance
        block_instance.save()
        return True

    def _save_image_block_type(self, block_instance, block_data):
        """
        If the block is of type image we save it by copying the contents from draft to the TextImageOption instance. 

        Args:
            block_instance (reflow_server.rich_text.models.Block): The Block instance saved.
            block_data (reflow_server.rich_text.services.data.BlockData): This is a handy class so we do not need to work with serializers
                                                                          or dict.

        Returns:
            bool: returns True indicating the file was saved
        """
        image_block_service = RichTextImageBlockService(block_instance.page_id, self.user_id, self.company_id)
        text_image_option_instance = image_block_service.save_image_block(
            block_instance.uuid, 
            block_data.image_file_uuid,
            block_data.image_link, 
            block_data.size_relative_to_view, 
            block_data.image_file_name,
            block_instance.image_option.id if block_instance.image_option else None
        )
        block_instance.image_option = text_image_option_instance
        block_instance.save()
        return True
    
    @transaction.atomic
    def remove_page(self, page_id):
        """
        Removes a page from the rich text. We need this to guarantee that files and other appended
        stuff are also removed when deleting the page. So please use this instead of updating the query
        directly.

        Args:
            page_id (int): A TextPage instance id to be removed.

        Returns:
            bool: returns True indicating the page was removed succesfully
        """
        page_instance = TextPage.objects.filter(
            id=page_id, 
            company_id=self.company_id, 
            user=self.user_id
        ).first()
        if page_instance:
            self.__remove_old_blocks_and_contents(page_instance, [], [])
            page_instance.delete()
        return True