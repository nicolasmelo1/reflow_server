from django.db import models

from reflow_server.pdf_generator.managers import PDFTemplateConfigurationPDFGeneratorManager


class PDFTemplateConfiguration(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500)
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'pdf_template_configuration'

    pdf_generator_ = PDFTemplateConfigurationPDFGeneratorManager()


class PDFTemplateConfigurationVariables(models.Model):
    pdf_template = models.ForeignKey('pdf_generator.PDFTemplateConfiguration', models.CASCADE, db_index=True,
                                     related_name='template_configuration_variables')
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'pdf_template_configuration_variables'


class PDFTemplateConfigurationRichText(models.Model):
    pdf_template = models.OneToOneField('pdf_generator.PDFTemplateConfiguration', models.CASCADE, db_index=True, 
                                        related_name='pdf_template_rich_text')
    rich_text = models.OneToOneField('rich_text.TextPage', models.CASCADE, db_index=True,
                                    related_name='rich_text_pdf_template')
    
    class Meta:
        db_table = 'pdf_template_configuration_rich_text'
