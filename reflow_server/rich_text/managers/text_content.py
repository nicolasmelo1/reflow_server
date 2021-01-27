from django.db import models


class TextContentRichTextManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
 
    def text_contents_by_page_id(self, page_id):
        """
        Gets all of the contents of a specific page 

        Args:
            page_id (int): The page intance id of what page does these contents belongs to

        Returns:
            django.db.models.QuerySet(reflow_server.rich_text.models.TextContent): A queryset of
            all of the TextContent intances from a specific page_id
        """
        return self.get_queryset().filter(block__page_id=page_id)
    
    def text_contents_by_page_id_excluding_content_ids(self, page_id, content_ids_to_exclude):
        """
        Gets all of the contents of a specific page without considering a list of content ids.

        Args:
            page_id (int): The page intance id of what page does these contents belongs to
            content_ids_to_exclude (list(int)): A list of content ids to exclude when querying

        Returns:
            Returns:
            django.db.models.QuerySet(reflow_server.rich_text.models.TextContent): A queryset of
            all of the TextContent intances from a specific page_id and that does not belong to
            a list of content ids.
        """
        return self.text_contents_by_page_id(page_id).exclude(id__in=content_ids_to_exclude)
    