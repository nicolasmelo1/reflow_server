from django.db import models


class RichTextTextBlockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def text_block_by_uuid_and_image_option_file_name(self, block_uuid, image_option_file_name):
        """
        Returns a single TextBlock instance by it's uuid and the image_option file_name. So this only works for blocks
        of type `image` that have a file saved. Otherwise this will not work.

        Args:
            block_uuid (str): This is a string that represents a uuid
            image_option_file_name (str): The name of the file

        Returns:
            reflow_server.rich_text.models.TextBlock: A single TextBlock instance that is returned if it matches the
                                                      criteria. Otherwise return None.
        """
        return self.get_queryset().filter(
            uuid = block_uuid,
            image_option__file_name=image_option_file_name
        ).first() 
    
    def text_blocks_by_page_id(self, page_id):
        return self.get_queryset().filter(page_id=page_id)
    
    def text_blocks_by_page_id_excluding_block_ids(self, page_id, block_ids_to_exclude):
        return self.text_blocks_by_page_id(page_id).exclude(id__in=block_ids_to_exclude)
    