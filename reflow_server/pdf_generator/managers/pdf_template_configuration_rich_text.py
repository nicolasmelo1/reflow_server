from django.db import models


class PDFTemplateConfigurationRichTextPDFGeneratorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def rich_text_page_id_by_pdf_template_configuration_id(self, pdf_template_configuration_id):
        """
        It's important to understand that it's not obligatory to use the RichText to create pdf templates.
        At least for the long run it will not be obligatory. 
        So this function is responsible for retriving the rich_text_id that a pdf_template_configuration_id 
        is bounded to

        Args:
            pdf_template_configuration_id (int): A reflow_server.pdf_generator.models.PDFTemplateConfiguration instance id

        Returns:
            int: Returns a reflow_server.rich_text.models.TextPage instance id.
        """
        return self.get_queryset().filter(pdf_template_id=pdf_template_configuration_id).values_list('rich_text_id', flat=True).first()

    def update_or_create(self, page_template_configuration_id, rich_text_page_id):
        """
        When we are saving a template that are bounded to a rich_text instance we need to bound both the
        PDFTemplateConfiguration and the TextPage using this method.

        Args:
            page_template_configuration_id (int): A reflow_server.pdf_generator.models.PDFTemplateConfiguration instance id
            rich_text_page_id (int): A reflow_server.rich_text.models.TextPage instance id

        Returns:
           reflow_server.pdf_generator.models.PDFTemplateConfigurationRichText: returns a PDFTemplateConfigurationRichText instance
        """
        instance, __ = self.get_queryset().update_or_create(
            pdf_template_id=page_template_configuration_id,
            defaults={
                'rich_text_id': rich_text_page_id
            }
        ) 
        return instance