from reflow_server.authentication.managers import company
from django.conf import settings

from reflow_server.draft.models import Draft
from reflow_server.data.models import Attachments
from reflow_server.core.utils.storage import Bucket
from reflow_server.draft.services import DraftService

import urllib


class AttachmentService:
    def __init__(self, company_id, user_id):
        """Service responsible for working with attachments in this application, most of the attachments logic should be found here
        """
        self.user_id = user_id
        self.company_id = company_id
        self.bucket = Bucket()

    def duplicate_attachment(self, duplicated_attachment_instance, to_duplicate_form_id, to_duplicate_field_id, to_duplicate_file_name, to_form_id, to_field_id):
        """
        This method duplicates the data from one attachment to the other. We need the duplicated attachment instance also
        so we can set the data like file_size and the url to the file.

        Args:
            duplicated_attachment_instance (reflow_server.data.models.Attachment): The duplicated Attachment instance
            so we can append the new `file_size` and `url` data to it.
            to_duplicate_form_id (int): The DynamicForm instance id you want to duplicate the attachment from.
            to_duplicate_field_id (int): The Field instance id that you want to duplicate the attachmente from
            to_duplicate_file_name (str): The actual file name that you want to duplicate for the other key.
            to_form_id (int): The new DynamicForm instance id of the attachment
            to_field_id (int):  The new Field instance id of the attachment

        Returns:
            reflow_server.data.models.Attachment: Returns the `duplicated_attachment_instance` already updated with the
            new data, or None. If None is returned it means an error has occured while duplicating. Since this is not our responsability to handle
            you should handle it where you are using.
        """
        to_duplicate = Attachments.data_.attachment_by_dynamic_form_id_field_id_and_file_name(
            to_duplicate_form_id, 
            to_duplicate_field_id, 
            str(to_duplicate_file_name)
        )
        if to_duplicate:
            new_key = "{file_attachments_path}/{id}/{field}/".format(
                id=str(to_form_id), 
                field=str(to_field_id), 
                file_attachments_path=settings.S3_FILE_ATTACHMENTS_PATH
            ) + str(to_duplicate_file_name)
            try:
                self.bucket.copy(
                    from_key="{file_attachments_path}/{id}/{field}/".format(
                        id=str(to_duplicate.form.id), 
                        field=str(to_duplicate.field.id), 
                        file_attachments_path=settings.S3_FILE_ATTACHMENTS_PATH
                    ) + str(to_duplicate.file),
                    to_key=new_key
                )
            except:
                return None

            url = self.bucket.get_temp_url(new_key)
            duplicated_attachment_instance.file_url = url.split('?')[0]
            duplicated_attachment_instance.file_size = to_duplicate.file_size
            duplicated_attachment_instance.save()

        return duplicated_attachment_instance


    def save_attachment(self, form_id, field_id, file_name):
        """
        Saves a new attachment based on the following parameters: `form_id`, `field_id` and `file_name`
        if an attachment have all of this criteria we will made an update, otherwise if no Attachment can be found 
        we will make an create.

        The file_data cannot always be present, because of this we consider this as default to None. it's important
        to understand however that if the file_data is not present we should fail the request since the file needs to
        be saved in order to work.

        Args:
            form_id (int): A DynamicForm instance id, this could be either a section_id or a main_form_id. This means
            this instance could either have depends_on parameter set to None or not.
            field_id (int): The id of the field from whom you are uploading this new attachment from.
            file_name (str): The name of the file, nothing much to say
            file_data (TemporaryUploadedFile, optional): This is optional but it's actually required for the hole upload to work
            since it's not this method responsability to check if the file has been uploaded, we can set it default as None. 
            Defaults to None.

        Returns:
            reflow_server.data.models.Attachment: The newly created or updated Attachment instance.
        """
        attachment_instance = Attachments.data_.attachment_by_dynamic_form_id_field_id_and_file_name(
            form_id, field_id, file_name
        )
    
        if not attachment_instance:
            attachment_instance = Attachments()
    
        attachment_instance.file = file_name
        attachment_instance.field_id = field_id
        attachment_instance.form_id = form_id

        #handles a simple insertion
        draft_id = DraftService.draft_id_from_draft_string_id(file_name)
        if draft_id != -1:
            draft_instance = Draft.data_.draft_by_draft_id_user_id_and_company_id(draft_id, self.user_id, self.company_id)
            file_size = draft_instance.file_size
            real_file_name = draft_instance.value
            bucket_key = "{file_attachments_path}/{id}/{field}/".format(
                id=str(form_id), 
                field=str(field_id), 
                file_attachments_path=settings.S3_FILE_ATTACHMENTS_PATH
            )

            draft_service = DraftService(self.company_id, self.user_id)
            url = draft_service.copy_file_from_draft_string_id_to_bucket_key(file_name, bucket_key)

            attachment_instance.file = real_file_name
            attachment_instance.file_url = url
            attachment_instance.file_size = file_size

        attachment_instance.save()

        return attachment_instance

    def get_attachment_url(self, dynamic_form_id, field_id, file_name):
        """
        For retrieving the attachment url we actually use the attachment file_url. We use this because if the key changes
        we will not run with any issues with it. We can make a further migration more easily and less painfuly by making 
        it this way.

        Args:
            dynamic_form_id (int): The main_form id. This is a DynamicForm instance id where depends_on is NOT NULL. This means
                                   this is NOT a section.
            field_id (int): Every attachment is bounded to the field id, that's why we need this. So we can know from which field_id
                            this attachment is from
            file_name (str): The actual name of the file you want the custom url from.

        Returns:
            str: This is the URL of the file. Be aware that this method can also return None if no attachment is found.
        """
        attachment = Attachments.data_.attachment_by_dynamic_form_id_field_id_and_file_name(dynamic_form_id, field_id, file_name)
        if attachment:
            if attachment.file_url and len(attachment.file_url.split('/{}/'.format(attachment.file_attachments_path)))>1:
                key = attachment.file_attachments_path + '/' + attachment.file_url.split('/{}/'.format(attachment.file_attachments_path))[1]
                key = urllib.parse.unquote(key)
            else:
                key = '{file_attachments_path}/{id}/{field}/{file_name}'.format(
                    id=attachment.form_id, field=attachment.field_id,
                    file_attachments_path=attachment.file_attachments_path,
                    file_name=attachment.file
                )
            return self.bucket.get_temp_url(key)
        else:
            return None