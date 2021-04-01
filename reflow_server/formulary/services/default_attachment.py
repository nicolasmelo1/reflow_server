from django.db import transaction
from django.conf import settings

from reflow_server.draft.services import DraftService
from reflow_server.core.utils.storage import Bucket
from reflow_server.formulary.models import DefaultFieldValue, DefaultFieldValueAttachments

import urllib


class DefaultAttachmentService:
    def __init__(self, company_id, user_id, field_id):
        self.field_id = field_id
        self.company_id = company_id
        self.user_id = user_id
        self.bucket = Bucket()
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def save_from_draft_string_id(self, draft_string_id, default_field_value_id, real_file_name, file_size):
        """
        Saves the draft to the DefaultAttachment, this is only used for bucket operation and for actually saving the model, 
        everything else is handled entirely in the FieldService.

        Args:
            draft_string_id (str): The draft_string_id recieved when you save a draft
            default_field_value_id (int): The DefaultFieldValue instance id
            real_file_name (str): The name of the file that was saved on the draft
            file_size (int): The size of the file that was saved on the draft

        Returns:
            reflow_server.formulary.models.DefaultFieldValueAttachments: The saved DefaultFieldValueAttachments instance
        """
        bucket_key = "{file_default_attachments_path}/{default_field_value_instance_id}/".format(
            file_default_attachments_path=settings.S3_FILE_DEFAULT_ATTACHMENTS_PATH,
            default_field_value_instance_id=default_field_value_id
        )

        file_url = DraftService(self.company_id, self.user_id)\
            .copy_file_from_draft_string_id_to_bucket_key(
                draft_string_id,
                bucket_key
            )

        default_field_value_attachment_instance = DefaultFieldValueAttachments.formulary_.update_or_create(
            file_name=real_file_name,
            file_url=file_url,
            file_size=file_size
        )
        return default_field_value_attachment_instance
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def remove_default_attachment(self, default_field_value_ids_to_keep):
        """
        Removes the default attachment files from the bucket.

        Args:
            default_field_value_ids_to_keep (list(int)): The list of DefultFieldValue instance ids to keep, the others, not present in this list,
            will be removed
        """
        default_field_values_to_delete = DefaultFieldValue.formulary_.default_field_values_by_field_id_excluding_default_field_value_ids(self.field_id, default_field_value_ids_to_keep)

        for default_field_value_to_delete in default_field_values_to_delete:
            bucket_key = "{file_default_attachments_path}/{default_field_value_instance_id}/".format(
                file_default_attachments_path=default_field_value_to_delete.default_attachment.file_default_attachments_path,
                default_field_value_instance_id=default_field_value_to_delete.id
            )
            self.bucket.delete(key=bucket_key)

    def __get_default_attachment_key(self, file_name):
        """
        Retrieves a key for a default_attachment file in a s3 bucket.

        Args:
            file_name (str): The name of the file to retrieve the key for

        Returns:
            str: The bucket key for the file
        """
        instance = DefaultFieldValue.formulary_.default_value_field_by_default_value_field_attachment_file_name_field_id_and_company_id(
            file_name=file_name,
            company_id=self.company_id,
            field_id=self.field_id
        )
        file_url = instance.default_attachment.file_url 
        file_default_attachments_path = instance.default_attachment.file_default_attachments_path
        key = None
        if file_url and len(file_url.split('/{}/'.format(file_default_attachments_path)))>1:
            key = file_default_attachments_path + '/' + file_url.split('/{}/'.format(file_default_attachments_path))[1]
            key = urllib.parse.unquote(key)
        else:
            key = "{file_default_attachments_path}/{default_field_value_instance_id}/".format(
                file_default_attachments_path=file_default_attachments_path,
                default_field_value_instance_id=instance.id
            )
        return key
    # ------------------------------------------------------------------------------------------
    def get_default_attachment_url(self, file_name):
        """
        Gets the temporary url for the file, we need this so we are able to display the file to the user.

        Args:
            file_name (str): The name of the file you want to retrieve

        Returns:
            str: The temporary url for the file.
        """
        return self.bucket.get_temp_url(self.__get_default_attachment_key(file_name))
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def get_draft_string_id_from_default_attachment(self, file_name, is_public=False):
        default_field_value_instance = DefaultFieldValue.formulary_.default_value_field_by_default_value_field_attachment_file_name_field_id_and_company_id(
            file_name=file_name,
            company_id=self.company_id,
            field_id=self.field_id
        )
        if default_field_value_instance:
            draft_instance = DraftService(self.company_id, self.user_id)
            key = self.__get_default_attachment_key(file_name)

            draft_string_id = draft_instance.copy_file_to_draft(
                key, 
                default_field_value_instance.default_attachment.file, 
                default_field_value_instance.default_attachment.file_size, 
                is_public
            )

            return draft_string_id
        else:
            return None