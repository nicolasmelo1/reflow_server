from django.conf import settings

from reflow_server.core.events import Event
from reflow_server.core.utils.storage import Bucket
from reflow_server.authentication.models import UserExtended

class UserService:
    def update_user(self, user_id, profile_image=None):
        """
        Responsible for updating a specific user. Right now we only update the profile image of the user. He cannot change anything else.
        """
        bucket = Bucket()
        instance = UserExtended.authentication_.user_by_user_id(user_id)
        
        if profile_image:
            key_path= "{user_profile_image_path}/{user_id}/".format(
                user_id=str(user_id),
                user_profile_image_path=settings.S3_USER_PROFILE_IMAGE_PATH
            )
            if instance.profile_image_url:
                file_name = instance.profile_image_url.split(key_path)[1]
                bucket.delete(
                    key=key_path+file_name
                )
            url = bucket.upload(
                key=key_path + str(profile_image[0].field_name).replace(' ', '-'),
                file=profile_image[0],
                is_public=True
            )
            instance.profile_image_url = url

        instance.save()
        
        # sends the events to the clients
        Event.register_event('user_updated', {
            'company_id': instance.company_id,
            'user_id': user_id
        })
        return instance