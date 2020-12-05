from django.db import models


class TextPagePDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def remove_text_page_by_rich_text_page_id_company_id_and_user_id(self, rich_text_page_id, company_id, user_id):
        return self.get_queryset().filter(id=rich_text_page_id, company_id=company_id, user_id=user_id).delete()