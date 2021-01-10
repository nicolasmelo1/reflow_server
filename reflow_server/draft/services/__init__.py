from django.conf import settings
from django.db import transaction

from reflow_server.core.utils.storage import Bucket
from reflow_server.draft.models import Draft, DraftType

import base64
import urllib

draft_id_template = 'draft-{}'

class DraftService:
    def __init__(self, company_id, user_id):
        """
        This is a service for handling all types of services. This might be the only and main service from
        this domain. As said on reflow_server.draft.models.Draft a draft is something that is temporary it's not
        something that will stick around for long. It's more like an auxiliary data. The user saves a data, and we save this
        for doing further operations in the future. If nothing is made we do nothing and the draft will be wiped.

        Args:
            company_id (int): Every draft is bounded to a Company instance and a UserExtended instance so we can 
                              still maintain the security of the draft that the users are saving.
            user_id (int): As said earlier, for securty reasons we bound every draft to a UserExtended instance.
        """
        self.bucket = Bucket()
        self.company_id = company_id
        self.user_id = user_id
    
    @transaction.atomic
    def save_new_draft(self, draft_file=None, draft_value=None, draft_id=None):
        """
        Method used for saving a draft. It can be a draft that already exists or some draft that does not exist yet. 
        To update a draft that already exists you might want to set the `draft_id` parameter.

        When saving a draft it's important to understand that wheather `draft_file` is defined it will be a Draft of
        `file` type. Otherwise if `draft_value` is defined, the draft will be of `value` type. It can be ONLY ONE or Another, 
        NEVER both. 

        Args:
            draft_file (TemporaryUploadedFile, optional): The uploaded file, as you might be aware already, we can only upload 
            one file at a time. Defaults to None.
            draft_value (str, optional): The draft value as a string, always as a string. If `draft_file` is set this should be None.
            Defaults to None.

        Returns:
            str: A draft_string_id. This `draft_string_id` is not trivial, it's a base64 encoded string. And you might ask yourself why do this instead of
            returning only the id of the saved draft. The reason is that we might use the draft before saving the real data, this means
            that when we save the actual data we need to check if the string recieved is a draft or not. If we use just an integer, this becomes
            kind of blurry. The odds to know if just an int is a draft are lower than to know if a special encoded string is a draft.
        """
        url = ''
        if draft_file:
            draft_type_id = DraftType.objects.filter(name='file').values_list('id', flat=True).first()
        else:
            draft_type_id = DraftType.objects.filter(name='value').values_list('id', flat=True).first()

        instance = Draft.draft_.create_or_update_draft(
            draft_id=draft_id,
            value = draft_file.name if draft_file else draft_value,
            draft_type_id = draft_type_id,
            file_size = draft_file.size if draft_file else None,
            user_id = self.user_id,
            company_id = self.company_id
        )

        if draft_file:
            # if you are updating a draft we need to delete the old draft and upload again.
            if instance.file_url and len(instance.file_url.split('/{}/'.format(instance.file_draft_path)))>1:
                key = instance.file_draft_path + '/' + instance.file_url.split('/{}/'.format(instance.file_draft_path))[1]
                key = urllib.parse.unquote(key)
                self.bucket.delete(key)
                
            url = self.bucket.upload(
                key="{file_draft_path}/{id}/".format(
                    id=str(instance.id), 
                    file_draft_path=settings.S3_FILE_DRAFT_PATH) + str(draft_file.name),
                file=draft_file
            )
            Draft.draft_.update_file_url_by_draft_id(instance.id, url)

        return base64.b64encode(draft_id_template.format(instance.id).encode('utf-8')).decode('utf-8')

    @transaction.atomic
    def copy_file_from_draft_string_id_to_bucket_key(self, draft_string_id, bucket_key, delete_after_copy=True):
        """
        This function uses the `draft_string_id` to copy a file from the draft bucket to another bucket (refer to `save_new_draft()`
        method on reference on what `draft_string_id` is). When we copy we understand that the draft is not needed anymore, so we 
        delete it. If you want to override this functionality, set `delete_after_copy` parameter to False.

        IMPORTANT: the key DOES NOT NEED to set the file_name, we set the file_name to the key you are copying to automatically.
        
        Args:
            draft_string_id (str): This `draft_string_id` is not trivial, it's a base64 encoded string. And you might ask yourself why do this instead of
            returning only the id of the saved draft. The reason is that we might use the draft before saving the real data, this means
            that when we save the actual data we need to check if the string recieved is a draft or not. If we use just an integer, this becomes
            kind of blurry. The odds to know if just an int is a draft are lower than to know if a special encoded string is a draft.
            bucket_key (str): The new key to copy the file to

        Returns:
            url: The new url of this new bucket location after the file has been copied from one place to another
        """

        draft_id = DraftService.draft_id_from_draft_string_id(draft_string_id)
        draft_instance = Draft.draft_.draft_file_by_draft_id_company_id_and_user_id(
            draft_id=draft_id, user_id=self.user_id, company_id=self.company_id
        )
        bucket_key = bucket_key + str(draft_instance.value)
        self.bucket.copy(
            from_key="{file_draft_path}/{id}/".format(
                id=str(draft_id), 
                file_draft_path=settings.S3_FILE_DRAFT_PATH
            ) + str(draft_instance.value),
            to_key=bucket_key
        )
        if delete_after_copy:
            self.bucket.delete(
                "{file_draft_path}/{id}/".format(
                    id=str(draft_id), 
                    file_draft_path=settings.S3_FILE_DRAFT_PATH
                ) + str(draft_instance.value)
            )
            draft_instance.delete()
        url = self.bucket.get_temp_url(bucket_key)
        url = url.split('?')[0]
        return url

    def draft_file_url_by_draft_string_id(self, draft_string_id):
        """
        Same as `.draft_file_url_by_draft_id()` method, except that this uses the `draft_string_id` and not the `draft_id`.

        Args:
            draft_string_id (str): This `draft_string_id` is not trivial, it's a base64 encoded string. And you might ask yourself why do this instead of
            returning only the id of the saved draft. The reason is that we might use the draft before saving the real data, this means
            that when we save the actual data we need to check if the string recieved is a draft or not. If we use just an integer, this becomes
            kind of blurry. The odds to know if just an int is a draft are lower than to know if a special encoded string is a draft.
            bucket_key (str): The new key to copy the file to

        Returns:
            str: returns a empty string if a the draft_id is not from a valid Draft instance. Otherwise return a url.
        """
        draft_id = DraftService.draft_id_from_draft_string_id(draft_string_id)
        return self.draft_file_url_by_draft_id(draft_id)

    def draft_file_url_by_draft_id(self, draft_id):
        """
        This creates the draft file url by the Draft instance id. This draft file url is the temporary url
        generated from the bucket to get the file.

        Args:
            draft_id (int): A Draft instance id.

        Returns:
            str: returns a empty string if a the draft_id is not from a valid Draft instance. Otherwise return a url.
        """
        draft_instance = Draft.draft_.draft_file_by_draft_id_company_id_and_user_id(
            draft_id=draft_id, user_id=self.user_id, company_id=self.company_id
        )  
        if draft_instance:
            if draft_instance.file_url and len(draft_instance.file_url.split('/{}/'.format(draft_instance.file_draft_path)))>1:
                key = draft_instance.file_draft_path + '/' + draft_instance.file_url.split('/{}/'.format(draft_instance.file_draft_path))[1]
                key = urllib.parse.unquote(key)
            else:
                key = '{file_draft_path}/{id}/{file_name}'.format(
                    id=draft_instance.id,
                    file_draft_path=draft_instance.file_draft_path,
                    file_name=draft_instance.value
                )
            url = self.bucket.get_temp_url(key)
            return url
        else:
            return ''
            
    @transaction.atomic
    def remove_draft_by_draft_id(self, draft_id):
        """
        Removes a draft by it's id (this is NOT the `draft_string_id`)

        Args:
            draft_id (int): The id of the Draft instance to remove, if it is a file
                            we remove the file from the storage service.

        Returns:
            bool: returns True indicating everything went fine
        """
        draft_instance_to_remove = Draft.draft_.draft_file_by_draft_id_company_id_and_user_id(
            draft_id=draft_id, user_id=self.user_id, company_id=self.company_id
        )  
        if draft_instance_to_remove:
            if draft_instance_to_remove.file_url:
                if draft_instance_to_remove.file_url and len(draft_instance_to_remove.file_url.split('/{}/'.format(draft_instance_to_remove.file_draft_path)))>1:
                    key = draft_instance_to_remove.file_draft_path + '/' + draft_instance_to_remove.file_url.split('/{}/'.format(draft_instance_to_remove.file_draft_path))[1]
                    key = urllib.parse.unquote(key)
                else:
                    key = '{file_draft_path}/{id}/{file_name}'.format(
                        id=draft_instance_to_remove.id,
                        file_draft_path=draft_instance_to_remove.file_draft_path,
                        file_name=draft_instance_to_remove.value
                    )
                
                self.bucket.delete(key)
            draft_instance_to_remove.delete()
        return True
            

    @staticmethod
    def draft_id_from_draft_string_id(draft_string_id):
        """
        A draft_string_id is just a base64 encoded string with `draft-{draft_id}` where `{draft_id}` is the id of the draft.
        So if the string can be decoded and it's content starts with `draft` we know it's definetly a draft, otherwise it's not a draft.
        If we used ints instead of strings this would be kind of blurry.

        Args:
            draft_string_id (str): the draft_string_id as explained `save_new_draft()` method.

        Returns:
            int: it returns either -1, indicating that THIS IS NOT a draft, or the id of the draft instance.
        """
        if draft_string_id not in [None, '']:
            try:
                draft_string_id = base64.b64decode(draft_string_id.encode('utf-8')).decode('utf-8')
                draft_id = int(draft_string_id.replace('draft-', ''))
                return draft_id
            except Exception as e:
                return -1
        else:
            return - 1

        