from django.db import models

from reflow_server.pdf_generator.managers import PDFTemplateConfigurationPDFGeneratorManager, \
    PDFTemplateConfigurationVariablesPDFGeneratorManager, PDFGeneratedPDFGeneratorManager, \
    PDFTemplateAllowedTextBlockPDFGeneratorManager
from reflow_server.pdf_generator.models.abstract import AbstractPDFTemplateConfiguration
from reflow_server.theme.managers import PDFTemplateAllowedTextBlockThemeManager, PDFTemplateConfigurationVariableThemeManager, \
    PDFTemplateConfigurationThemeManager


class PDFTemplateAllowedTextBlock(models.Model):
    """
    These are the allowed blocks that can exist inside of the pdf. Other blocks are not permitted.
    """
    block = models.ForeignKey('rich_text.TextBlockType', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'pdf_template_allowed_text_block'

    pdf_generator_ = PDFTemplateAllowedTextBlockPDFGeneratorManager()
    theme_ = PDFTemplateAllowedTextBlockThemeManager()

class PDFTemplateConfiguration(AbstractPDFTemplateConfiguration):
    """
    This model holds the template configuration data. You will notice some small things.
    First this is not obligatory bounded to the rich_text TextPage. The templates holds some basic information
    about the template like the name of the template, the company that it is bounded to, the user
    and the formulary.
    """
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'pdf_template_configuration'
        ordering = ('-updated_at',)

    objects = models.Manager()
    pdf_generator_ = PDFTemplateConfigurationPDFGeneratorManager()
    theme_ = PDFTemplateConfigurationThemeManager()


class PDFTemplateConfigurationVariables(models.Model):
    """
    This is each variable of the PDF Configuration template. Each variable here is unordered, we just
    use this to know what fields we should use in a template. So we can improve the performance when retrieiving
    the data.
    """
    pdf_template = models.ForeignKey('pdf_generator.PDFTemplateConfiguration', models.CASCADE, db_index=True,
                                     related_name='template_configuration_variables')
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'pdf_template_configuration_variables'

    objects = models.Manager()
    pdf_generator_ = PDFTemplateConfigurationVariablesPDFGeneratorManager()
    theme_ = PDFTemplateConfigurationVariableThemeManager()


class PDFGenerated(models.Model):
    """
    Each generated PDF, this is used to contain all of the downloads of a pdf from a user, so we can know which user, from
    which company and which pdf template was selected for downloading. This is mostly for billing, we usually bill the user
    on PDFs by the number of downloads he makes, not on the number of templates that he has.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    pdf_template = models.ForeignKey('pdf_generator.PDFTemplateConfiguration', models.CASCADE, db_index=True)
    
    class Meta:
        db_table = 'pdf_generated'

    pdf_generator_ = PDFGeneratedPDFGeneratorManager()
    