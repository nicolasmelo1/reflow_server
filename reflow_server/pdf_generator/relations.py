from re import L
from rest_framework import serializers

from reflow_server.pdf_generator.models import PDFTemplateConfigurationVariables, \
    PDFTemplateConfigurationRichText
    

class PDFTemplateConfigurationVariablesRelation(serializers.ModelSerializer):
    class Meta:
        model = PDFTemplateConfigurationVariables
        fields = ('field',)


class PDFTemplateConfigurationRichTextRelation(serializers.ModelSerializer):
    class Meta:
        model = PDFTemplateConfigurationRichText
        fields = ('rich_text',)