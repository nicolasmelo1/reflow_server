from django.conf import settings
from django.db import transaction

from reflow_server.draft.services import DraftService
from reflow_server.draft.models import Draft
from reflow_server.rich_text.models import TextBlock, TextImageOption
from reflow_server.core.utils.storage import Bucket

import urllib


class RichTextImageBlockService:
    def __init__(self, page_id, user_id, company_id):
        """
        Service responsible for handling when blocks are of type `image`. Handles everything about `image` blocks
        from saving to creating a generating a temporary url to the file in the storage service the file resies in.

        Args:
            page_id (int): A rich text TextPage instance id. This is the id of the page this block resides in.
            user_id (int): A UserExtended instance id. This is the user that is requesting to access this type of data. We need this
                           so we can prevent unwanted users from using and accessing this data.
            company_id (int): A Company instance id. Same as a UserExtended.
        """
        self.bucket = Bucket()
        self.page_id = page_id
        self.user_id = user_id
        self.company_id = company_id

    def get_image_url(self, block_uuid, file_name):
        """
        Returns a temporary url of the image from our storage directly to the client.

        Args:
            block_uuid (str): The uuid of the block that holds the image you are trying to retrieve.
            file_name (str): The name of the file you are trying to retrieve the url from

        Returns:
            str: A temporary url for the file.
        """
        block_instance = TextBlock.rich_text_.text_block_by_uuid_and_image_option_file_name(block_uuid, file_name) 
        if block_instance:
            if block_instance.image_option.file_url and len(block_instance.image_option.file_url.split('/{}/'.format(block_instance.image_option.file_image_path)))>1:
                key = block_instance.image_option.file_image_path + '/' + block_instance.image_option.file_url.split('/{}/'.format(block_instance.image_option.file_image_path))[1]
                key = urllib.parse.unquote(key)
            else:
                key = '{file_rich_text_image_path}/{block_uuid}/{file_name}'.format(
                    id=block_uuid,
                    file_rich_text_image_path=block_instance.image_option.file_image_path,
                    file_name=block_instance.image_option.file_name
                )
            url = self.bucket.get_temp_url(key)
            return url
        else:
            return ''

    @transaction.atomic
    def save_image_block(self, block_uuid, image_link=None, size_relative_to_view=1, image_file_name=None, image_option_id=None):
        """
        A helper method to save the `image` block type. If the user is uploading a file he needs to save this file to draft BEFORE saving. The draft_string_id will 
        be appended to file_name, so we always need to check if the file_name is a draft. If it is we copy the contents of the draft to here.

        Args:
            block_uuid (str): The uuid of the block that will hold the image data.
            image_link (str, optional): If the image is from an external source we need this to show on the user. If it's from an external source we DO NOT do any kind of protection. 
                                        Defaults to None.
            size_relative_to_view (int, optional): This is the size relative to view, 1 assumes it's the hole width, a 0.5 assumes it'll be half of the width. Defaults to 1.
            image_file_name (str, optional): If the user is saving a image directly from his computer, we need this. Defaults to None.
            image_option_id (int, optional): A TextImageOption instance id. Defaults to None.

        Returns:
            reflow_server.rich_text.models.TextOptionImage: A TextOptionImage instance that was created or updated, you will probably use this to append it to the block.
        """
        url = None
        file_name = None
        file_size = None
        # if we are editing, does not set file_name, file_size and url to null, otherwise pick
        # the instance you are updating and use those values already saved.
        if image_option_id:
            text_image_option_instance = TextImageOption.rich_text_.text_image_option_by_text_image_option_id(image_option_id)
            url = text_image_option_instance.file_url
            file_name = text_image_option_instance.file_name
            file_size = text_image_option_instance.file_size

        if image_file_name not in ['',  None]:
            draft_id = DraftService.draft_id_from_draft_string_id(image_file_name)
            if DraftService.draft_id_from_draft_string_id(image_file_name) != -1:
                draft_instance = Draft.rich_text_.draft_by_draft_id_user_id_and_company_id(draft_id, self.user_id, self.company_id)
                file_size = draft_instance.file_size
                file_name = draft_instance.value
                bucket_key = "{file_rich_text_image_path}/{block_uuid}/".format(
                    block_uuid=str(block_uuid), 
                    file_rich_text_image_path=settings.S3_FILE_RICH_TEXT_IMAGE_PATH
                )

                draft_service = DraftService(self.company_id, self.user_id)
                url = draft_service.copy_file_from_draft_string_id_to_bucket_key(image_file_name, bucket_key)

        text_image_option_instance = TextImageOption.rich_text_.update_or_create(
            size_relative_to_view, 
            image_link, 
            url,
            file_size,
            file_name,
            image_option_id,
        )
        return text_image_option_instance

    def remove_image_block(self, block_instance):
        """
        When the user deletes removes an image block and saves what we gotta do is delete the image
        file from s3. Since we do not do this automatically we need to do this by hand. So what does we do
        is that when a user removes a page or anything we go through all of the removed blocks and check
        if any of them has special cases when the block is being deleted. Then we remove the block from the database.
        
        On image blocks, our special case is to remove the image from s3. And that's exactly
        what we do in this method. It's nice to notice however, this is only needed if `file_name` is defined
        in the TextImageOption instance. Because if this is not None, it means a file was saved and no link was used.

        Args:
            block_instance (reflow_server.rich_text.models.TextBlock): The TextBlock instance that will be removed.

        Returns:
            bool: returns True indicating that the file was deleted from s3 and can be safely deleted from the database.
        """
        if block_instance and \
           block_instance.image_option and \
           block_instance.image_option.file_name:
            if block_instance.image_option.file_url:
                if block_instance.image_option.file_url and len(block_instance.image_option.file_url.split('/{}/'.format(block_instance.image_option.file_image_path)))>1:
                    key = block_instance.image_option.file_image_path + '/' + block_instance.image_option.file_url.split('/{}/'.format(block_instance.image_option.file_image_path))[1]
                    key = urllib.parse.unquote(key)
                else:
                    key = '{file_rich_text_image_path}/{block_uuid}/{file_name}'.format(
                        block_uuid=block_instance.uuid,
                        file_rich_text_image_path=block_instance.image_option.file_image_path,
                        file_name=block_instance.image_option.file_name
                    )
                
                self.bucket.delete(key)
        return True