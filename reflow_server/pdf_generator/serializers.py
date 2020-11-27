from rest_framework import serializers

from reflow_server.formulary.models import Field
from reflow_server.pdf_generator.models import PDFTemplateConfiguration
from reflow_server.pdf_generator.relations import PDFTemplateConfigurationVariablesRelation, \
    PDFTemplateConfigurationRichTextRelation


class PDFTemplateConfigurationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    template_configuration_variables = PDFTemplateConfigurationVariablesRelation(many=True)
    pdf_template_rich_text = PDFTemplateConfigurationRichTextRelation()

    class Meta:
        model = PDFTemplateConfiguration
        fields = ('id', 'name', 'template_configuration_variables', 'pdf_template_rich_text')
    
class FieldOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'label_name', 'name')