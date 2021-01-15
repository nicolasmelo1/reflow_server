from django.db import models


class RichTextTextBlockManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def text_block_by_file_image_uuid(self, file_image_uuid):
        """
        Returns a single TextBlock instance by it's uuid and the image_option file_name. So this only works for blocks
        of type `image` that have a file saved. Otherwise this will not work.

        Args:
            file_image_uuid (str): The uuid of the image file you have saved, we use this uuid so the user can duplicate freely the images.

        Returns:
            reflow_server.rich_text.models.TextBlock: A single TextBlock instance that is returned if it matches the
                                                      criteria. Otherwise return None.
        """
        return self.get_queryset().filter(
            image_option__file_image_uuid=file_image_uuid
        ).first() 
    
    def text_blocks_by_page_id(self, page_id):
        return self.get_queryset().filter(page_id=page_id)
    
    def text_blocks_by_page_id_excluding_block_ids(self, page_id, block_ids_to_exclude):
        return self.text_blocks_by_page_id(page_id).exclude(id__in=block_ids_to_exclude)
    