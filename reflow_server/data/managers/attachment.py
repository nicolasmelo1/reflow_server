from django.db import models
from django.db.models import Q, Sum


class AttachmentsDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def attachment_by_dynamic_form_id_field_id_and_file_name(self, dynamic_form_id, field_id, file_name):
        """
        This retrieves a single attachment based on the dynamic_form_id, field_id and the file_name.
        It is important to notice that `dynamic_form_id` parameter can be the a section_id or a formulary_id.

        Args:
            dynamic_form_id (int): This dynamic_form_id is the id of a section or a formulary.
            field_id (int): The field id of this attachment.
            file_name (str): The file_name of the attachment.

        Returns:
            reflow_server.data.models.Attachment: Retrieves a single attachment based on the parameters recieved. 
        """
        return self.get_queryset().filter(Q(form__depends_on_id=dynamic_form_id) | Q(form_id=dynamic_form_id))\
            .filter(field_id=field_id, file=file_name).first()
