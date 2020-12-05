from django.db import models


class PDFTemplateConfigurationRichTextPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def rich_text_page_id_by_pdf_template_configuration_id(self, pdf_template_configuration_id):
        return self.get_queryset().filter(pdf_template_id=pdf_template_configuration_id).values_list('rich_text_id', flat=True).first()

    def update_or_create(self, page_template_configuration_id, rich_text_page_id):
        instance, __ = self.get_queryset().update_or_create(
            pdf_template_id=page_template_configuration_id,
            defaults={
                'rich_text_id': rich_text_page_id
            }
        ) 
        return instance