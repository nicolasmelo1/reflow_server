from rest_framework import serializers

from reflow_server.formulary.models import Field
from reflow_server.pdf_generator.models import PDFTemplateConfigurationVariables


class PDFTemplateConfigurationVariablesRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = PDFTemplateConfigurationVariables
        fields = ('id', 'field')


class FieldOptionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = Field.pdf_generator_.fields_by_main_form_id(data.core_filters['form'].id)
        return super(FieldOptionListSerializer, self).to_representation(data) 


class FieldOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = Field
        list_serializer_class = FieldOptionListSerializer
        fields = ('id', 'name', 'label_name')