from django.db import models


class TextPagePDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def remove_text_page_by_rich_text_page_id_company_id_and_user_id(self, rich_text_page_id, company_id, user_id):
        """
        This removes a TextPage instance by the page id.

        Args:
            rich_text_page_id (int): The reflow_server.rich_text.models.TextPage instance id to be removed.
            user_id (int): A reflow_server.authentication.models.UserExtended instance id
            company_id (int): A reflow_server.authentication.models.Company instance id

        Returns:
            int: The number of removed instances
        """
        return self.get_queryset().filter(id=rich_text_page_id, company_id=company_id, user_id=user_id).delete()