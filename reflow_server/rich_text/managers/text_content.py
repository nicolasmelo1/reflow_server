from django.db import models


class RichTextTextContentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
 
    def text_contents_by_page_id(self, page_id):
        return self.get_queryset().filter(block__page_id=page_id)
    
    def text_contents_by_page_id_excluding_content_ids(self, page_id, content_ids_to_exclude):
        return self.text_contents_by_page_id(page_id).exclude(id__in=content_ids_to_exclude)
    