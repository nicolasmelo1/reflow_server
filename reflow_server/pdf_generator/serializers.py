from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.data.models import FormValue
from reflow_server.formulary.models import Form, Field
from reflow_server.pdf_generator.models import PDFTemplateConfiguration, PDFTemplateAllowedTextBlock
from reflow_server.pdf_generator.relations import PDFTemplateConfigurationVariablesRelation, \
    FieldOptionRelation
from reflow_server.pdf_generator.relations.rich_text import PageRelation
from reflow_server.pdf_generator.services import PDFGeneratorService
from reflow_server.pdf_generator.services.data import PDFVariablesData
from reflow_server.rich_text.services import ordered_list_from_serializer_data_for_page_data, PageData
from reflow_server.rich_text.services.exceptions import RichTextValidationException

import re

class PDFTemplateConfigurationManySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField()

    class Meta:
        model = PDFTemplateConfiguration
        fields = ('id', 'name')


class PDFTemplateConfigurationSerializer(serializers.ModelSerializer):
    """
    The templates serializer, this holds the data needed for rendering pdf templates.
    Two parts are important:
    - The rich text data, which is not obligatory to create a pdf template.
    - The template configuration variables, that holds the field_ids to use as variables inside
    of the template.

    This is used when editing a template but also when building the template for download.
    """
    id = serializers.IntegerField(allow_null=True)
    template_configuration_variables = PDFTemplateConfigurationVariablesRelation(many=True)
    name = serializers.CharField(error_messages={'null': 'blank', 'blank': 'blank'})
    rich_text_page = PageRelation()

    def is_valid(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name
        return super().is_valid()

    def validate(self, data):
        """
        Be aware that we first need to convert the rich text data to a data used by the RichText service
        and second we need to convert the PDFVariables to a object that will be used by the PDFTemplateConfigurationService.

        Args:
            user_id (int): The id of the UserExtended instance that is saving this template. Each template
                           is bounded to a user, and him, and only him can edit this pdf template that he is creating.
            company_id (int): When retrieving the templates. We retrieve the templates created by the hole company, and not only
                              the user. This is different on how dashboards, notifications and kanban works. You don't set the 
                              templates to public, but they are ALWAYS public here.
            form_name (str): From which form is this template. Obviously each template is bounded
                             to a form so we can use the fields of this form as variables for our template.
        """
        try:
            allowed_block_ids_for_pdf = PDFTemplateAllowedTextBlock.pdf_generator_.all_pdf_template_allowed_text_block_ids()
            self.pdf_variables_data = PDFVariablesData(self.instance.id if self.instance else None)
            self.pdf_generator_service = PDFGeneratorService(self.user_id, self.company_id, self.form_name)
            self.page_data = None

            # just adds the rich text data to a reflow_server.rich_text.services.data.PageData object so we can use it further for saving.
            if data.get('rich_text_page', None): 
                self.page_data = PageData(page_id=data.get('rich_text_page', {}).get('id', None), allowed_blocks=allowed_block_ids_for_pdf)
                blocks_to_add = ordered_list_from_serializer_data_for_page_data(data.get('rich_text_page'))
            
                for block in blocks_to_add:
                    block_data = self.page_data.add_block(block['data']['uuid'], block['data']['block_type'].id, block['depends_on_uuid'])
                    
                    if block['data']['block_type'].name == 'text' and block['data']['text_option']:
                        block_data.append_text_block_type_data(block['data']['text_option']['alignment_type'].id)
                    elif block['data']['block_type'].name == 'image' and block['data']['image_option']:
                        block_data.append_image_block_type_data(
                            block['data']['image_option']['file_image_uuid'],
                            block['data']['image_option']['link'], 
                            block['data']['image_option']['file_name'],
                            block['data']['image_option']['size_relative_to_view']
                        )
                    elif block['data']['block_type'].name == 'table' and block['data']['table_option']:
                        block_data.append_table_block_type_data(
                            block['data']['table_option']['border_color'],
                            block['data']['table_option']['text_table_option_column_dimensions'],
                            block['data']['table_option']['text_table_option_row_dimensions']
                        )
                    
                    for content in block['data'].get('rich_text_block_contents', []):
                        is_to_ignore_content = False
                        # Adds the variables here, on front end it was causing problems
                        if content.get('is_custom', False) and re.search('fieldVariable-\d+', content.get('custom_value', '')):
                            variable_field_id = re.match('fieldVariable-\d+', content.get('custom_value', '')).group(0)
                            variable_field_id = int(variable_field_id.replace('fieldVariable-', ''))
                            if Field.pdf_generator_.exist_field_by_id_and_company_id(variable_field_id, self.company_id):
                                self.pdf_variables_data.add_variable(variable_field_id)
                            else:
                                is_to_ignore_content = True
                                
                        if not is_to_ignore_content:
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
        except RichTextValidationException as rtve:
            raise serializers.ValidationError(detail={'detail': 'rich_text_not_valid', 'reason': 'invalid_rich_text'})
        
        return data

    def save(self):
        """
        Be aware that we first need to convert the rich text data to a data used by the RichText service
        we do this in the validate method inside of the serializer

        Returns:
            reflow_server.pdf_generator.models.PDFTemplateConfiguration: The newly created or updated PDFTemplateConfiguration instance.
            from the database.
        """

        return self.pdf_generator_service.save_pdf_template(
            name=self.validated_data['name'], 
            pdf_variables_data=self.pdf_variables_data,
            page_data=self.page_data, 
            pdf_template_id=self.instance.id if self.instance else None
        )

    class Meta:
        model = PDFTemplateConfiguration
        fields = ('id', 'name', 'template_configuration_variables', 'rich_text_page')


class FormFieldOptionsSerializer(serializers.ModelSerializer):
    """
    This is the serializer used for showing the fields that you can use as variables
    in the PDFTemplate. The fields are bounded to its formularies.
    """
    form_fields = FieldOptionRelation(many=True)
    form_from_connected_field = serializers.SerializerMethodField()

    def get_form_from_connected_field(self, obj):
        if self.context['form_from_connected_field_helper'].get(obj.id, None):
            return FieldOptionRelation(self.context['form_from_connected_field_helper'][obj.id].pop()).data
        else:
            return None

    class Meta:
        model = Form
        fields = ('id', 'label_name', 'form_name', 'form_fields', 'form_from_connected_field')


class FieldValueSerializer(serializers.ModelSerializer):
    """
    Similar to FormFieldOptionsSerializer, except it is for showing the data values
    of the fields of a form_id.
    """
    id = serializers.IntegerField(required=False, allow_null=True)
    value = ValueField(source='id')
    form_value_from_connected_field = serializers.SerializerMethodField()
    field_type = serializers.CharField(source='field_type.type')
    form_name = serializers.CharField(source='form.form.depends_on.form_name')

    def get_form_value_from_connected_field(self, obj):
        if self.context['form_value_from_connected_field_helper'].get(obj.id, None):
            field_to_use = self.context['form_value_from_connected_field_helper'][obj.id].pop()
            return FieldOptionRelation(field_to_use).data
        else:
            return None

    class Meta:
        model = FormValue
        fields = ('id', 'value', 'field_id', 'form_id', 'form_name', 'field_type', 'form_value_from_connected_field')


class PDFTemplateAllowedTextBlockSerializer(serializers.ModelSerializer):
    """
    The serializer responsible for handling the allowed blocks of a PDF template. If a PDF template was built with the rich text
    and the rich text contains any block outside this scope, the user will not be able to save.
    """
    class Meta:
        model = PDFTemplateAllowedTextBlock
        fields = ('block',)