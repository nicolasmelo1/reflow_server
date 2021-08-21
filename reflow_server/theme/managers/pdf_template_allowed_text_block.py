from django.db import models


class PDFTemplateAllowedTextBlockThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def all_pdf_template_allowed_text_blocks(self):
        """
        Gets all of the PDFTemplateAllowedTextBlock instances

        Returns:
            django.db.models.QuerySet(reflow_server.pdf_generator.models.PDFTemplateAllowedTextBlock): Returns all of the allowed blocks 
            that can exist in a PDFTemplate
        """
        return self.get_queryset().all()

    def all_pdf_template_allowed_text_block_ids(self):
        """
        Gets all of the block instance ids that the PDFTemplates can contain

        Returns:
            django.db.models.QuerySet(int): Returns all of the allowed block_ids that can exist in a PDFTemplate
        """
        return self.all_pdf_template_allowed_text_blocks().values_list('block_id', flat=True)