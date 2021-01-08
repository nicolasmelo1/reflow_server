from django.conf import settings

from reflow_server.draft.services import DraftService
from reflow_server.draft.models import Draft

from reflow_server.rich_text.services.data import PageData
from reflow_server.rich_text.services.utils import ordered_list_from_serializer_data_for_page_data
from reflow_server.rich_text.services.block import RichTextImageBlockService
from reflow_server.rich_text.models import TextContent, TextPage, TextBlock, TextTextOption, \
    TextImageOption


class RichTextBlockException(NotImplementedError):
    pass


class RichTextService:
    def __init__(self, company_id, user_id):
        self.company_id = company_id
        self.user_id = user_id

    def __remove_old_blocks_and_contents(self, page_instance, block_instances, content_instances):
        """
        Removes the blocks and contents that were removed from the rich_text.

        Args:
            page_instance (reflow_server.rich_text.models.TextPage): The saved text_page instance we use this to filter the blocks from this page.
            block_instances (list(reflow_server.rich_text.models.TextBlock)): The saved block instances, we use this to exclude all of the saved block 
            instances from the filter so we can delete the one's from the page but not on this list.
            content_instances (list(reflow_server.rich_text.models.TextContent)): Same as the block_instances but instead we filter from the block_instances
            and removes the content_instances from the filter, this way we can remove the contents that were removed from the database.

        Returns:
            bool: returns True to indicate everything was deleted.
        """
        TextBlock.objects.filter(page=page_instance).exclude(id__in=[block_instance.id for block_instance in block_instances]).delete()
        TextContent.objects.filter(block__in=block_instances)\
            .exclude(id__in=[content_instance.id for content_instance in content_instances]).delete()
        return True

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
            block_data.image_link, 
            block_data.size_relative_to_view, 
            block_data.image_file_name,
            block_instance.image_option.id if block_instance.image_option else None
        )
        block_instance.image_option = text_image_option_instance
        block_instance.save()
        return True
        