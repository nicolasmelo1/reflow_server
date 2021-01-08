from django.db import models

from reflow_server.pdf_generator.managers import PDFTemplateConfigurationPDFGeneratorManager, \
    PDFTemplateConfigurationVariablesPDFGeneratorManager, PDFGeneratedPDFGeneratorManager


class PDFTemplateConfiguration(models.Model):
    """
    This model holds the template configuration data. You will notice some small things.
    First this is not obligatory bounded to the rich_text TextPage. The templates holds some basic information
    about the template like the name of the template, the company that it is bounded to, the user
    and the formulary.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500)
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    rich_text_page = models.ForeignKey('rich_text.TextPage', models.CASCADE, db_index=True, null=True)

    class Meta:
        db_table = 'pdf_template_configuration'

    pdf_generator_ = PDFTemplateConfigurationPDFGeneratorManager()


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

    pdf_generator_ = PDFTemplateConfigurationVariablesPDFGeneratorManager()


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