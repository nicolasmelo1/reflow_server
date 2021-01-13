from django.db import models 


class RichTextTextImageOptionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def text_image_option_by_text_image_option_id(self, text_image_option_id):
        """
        Returns a single TextImageOption instance by it's id.

        Args:
            text_image_option_id (str): A TextImageOption instance id

        Returns:
            reflow_server.rich_text.models.TextImageOption: The TextImageOption instance that matches the id.
        """
        return self.get_queryset().filter(id=text_image_option_id).first()

    def update_or_create(self, size_relative_to_view=1, link=None, file_url=None, file_size=None, file_name=None, text_image_option_id=None):
        """
        Updates or creates a TextImageOption instance in the database. If `text_image_option_id` is defined we update the instance, otherwise
        we just create a new one.

        Args:
            size_relative_to_view (int, optional): This is the size relative to the view of the image in the front-end. Defaults to 1.
            link (str, optional): If the image is from a external source we use this link, otherwise this should be none. Defaults to None.
            file_url (str, optional): The url to the file in our storage service, this is only required if the user uploaded a file. Defaults to None.
            file_size (int, optional): The size of the file in bytes, only required if the user uploaded a file. Defaults to None.
            file_name (str, optional): The name of the file. Only required if the user uploaded a file. Defaults to None.
            text_image_option_id (int, optional): A TextImageOption instance id. This is only needed if you want to update an instance
                                                  that already exists. Defaults to None.

        Returns:
            reflow_server.rich_text.models.TextImageOption: A created or updated TextImageOption instance.
        """
        instance, __ = self.get_queryset().update_or_create(
            id=text_image_option_id,
            defaults={
                'size_relative_to_view': size_relative_to_view,
                'link': link,
                'file_url': file_url,
                'file_size': file_size,
                'file_name': file_name
            }
        )
        return instance