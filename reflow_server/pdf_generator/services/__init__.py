from django.db import transaction

from reflow_server.pdf_generator.models import PDFTemplateConfiguration, PDFTemplateConfigurationRichText, \
    PDFTemplateConfigurationVariables
from reflow_server.pdf_generator.services.data import PDFVariablesData
from reflow_server.formulary.models import Form, Field
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.rich_text.services import RichTextService


class PDFGeneratorService:
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form = Form.pdf_generator_.formulary_id_by_company_id_and_form_name(company_id, form_name).first()

    @property
    def form_options_to_use_on_template(self):
        form_options = [self.form]
        formulary_service = FormularyService(self.user_id, self.company_id)
        form_ids_the_user_has_access_to = formulary_service.formulary_ids_the_user_has_access_to
        form_fields = Field.pdf_generator_.form_fields_by_main_form_id_and_company_id(self.form.id, self.company_id)
        for field in form_fields:
            if field.form_field_as_option.form.depends_on_id in form_ids_the_user_has_access_to:
                form_options.append(field.form_field_as_option.form.depends_on)
        
        return form_options

    @transaction.atomic
    def save_pdf_template(self, name, pdf_variables_data, page_data=None, pdf_template_id=None):
        pdt_template_configuration_instance = PDFTemplateConfiguration.pdf_generator_.update_or_create_pdf_template_configuration(
            name, self.company_id, self.user_id, self.form.id, pdf_template_id
        )

        # adds the variables and deletes the removed variables.
        pdf_template_configuration_variable_ids = []
        for pdf_variable in pdf_variables_data.variables: 
            pdf_template_configuration_variable_instance = PDFTemplateConfigurationVariables.pdf_generator_.update_or_create(
                pdf_variable.field_id, pdt_template_configuration_instance.id, pdf_variable.variable_id
            )
            pdf_template_configuration_variable_ids.append(pdf_template_configuration_variable_instance.id)

        PDFTemplateConfigurationVariables.pdf_generator_.delete_pdf_template_configuration_variables_from_pdf_template_id_excluding_variable_ids(
            pdt_template_configuration_instance.id, pdf_template_configuration_variable_ids
        )

        if page_data:
            rich_text_service = RichTextService(self.company_id, self.user_id)
            rich_text_page_instance = rich_text_service.save_rich_text(page_data)
            PDFTemplateConfigurationRichText.pdf_generator_.update_or_create(
                pdt_template_configuration_instance.id, rich_text_page_instance.id
            )
            

        return pdt_template_configuration_instance