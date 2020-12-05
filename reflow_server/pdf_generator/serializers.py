from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.data.models import FormValue
from reflow_server.formulary.models import Form
from reflow_server.pdf_generator.models import PDFTemplateConfiguration
from reflow_server.pdf_generator.relations import PDFTemplateConfigurationVariablesRelation, \
    PDFTemplateConfigurationRichTextRelation, FieldOptionRelation
from reflow_server.pdf_generator.services import PDFGeneratorService, PDFVariablesData
from reflow_server.rich_text.services import ordered_list_from_serializer_data_for_page_data, PageData


class PDFTemplateConfigurationSerializer(serializers.ModelSerializer):
    """
    Gets the configuration of the template
    """
    id = serializers.IntegerField(allow_null=True)
    template_configuration_variables = PDFTemplateConfigurationVariablesRelation(many=True)
    pdf_template_rich_text = PDFTemplateConfigurationRichTextRelation()

    def save(self, user_id, company_id, form_name):
        pdf_generator_service = PDFGeneratorService(user_id, company_id, form_name)
        page_data = None

        # just adds the rich text data to a reflow_server.rich_text.services.data.PageData object so we can use it further for saving.
        if self.validated_data.get('pdf_template_rich_text', {}).get('rich_text', None): 
            page_data = PageData(page_id=self.validated_data.get('pdf_template_rich_text', {}).get('rich_text', {}).get('id', None))
            blocks_to_add = ordered_list_from_serializer_data_for_page_data(self.validated_data.get('pdf_template_rich_text', {}).get('rich_text'))
        
            for block in blocks_to_add:
                block_data = page_data.add_block(block['data']['uuid'], block['data']['block_type'].id, block['depends_on_uuid'])
                
                if block['data']['block_type'].name == 'text':
                    block_data.append_text_block_type_data(block['data']['text_option']['alignment_type'])
                
                for content in block['data'].get('rich_text_block_contents', []):
                    block_data.add_content(
                        content['uuid'], 
                        content.get('text', ''), 
                        content.get('is_bold', False),
                        content.get('is_italic', False),
                        content.get('is_underline', False),
                        content.get('is_code', False),
                        content.get('is_custom', False),
                        content.get('custom_value', None),
                        content.get('latex_equation', None),
                        content.get('marker_color', None),
                        content.get('text_color', None),
                        content.get('text_size', 12),
                        content.get('link', None)
                    )
        #PDF variable
        pdf_variables_data = PDFVariablesData()
        for variable in self.validated_data.get('template_configuration_variables', []):
            if variable.get('field', None):
                pdf_variables_data.add_variable(variable.get('id', None), variable['field'].id)

        return pdf_generator_service.save_pdf_template(
            name=self.validated_data['name'], 
            pdf_variables_data=pdf_variables_data,
            page_data=page_data, 
            pdf_template_id=self.instance.id if self.instance else None
        )


    class Meta:
        model = PDFTemplateConfiguration
        fields = ('id', 'name', 'template_configuration_variables', 'pdf_template_rich_text')


class FormFieldOptionsSerializer(serializers.ModelSerializer):
    form_fields = FieldOptionRelation(many=True)

    class Meta:
        model = Form
        fields = ('id', 'label_name', 'form_name', 'form_fields')


class FieldValueSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    value = ValueField(source='*')

    class Meta:
        model = FormValue
        fields = ('id', 'value', 'field_id')