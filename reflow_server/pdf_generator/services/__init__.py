from reflow_server.formulary.models import Form, Field
from reflow_server.formulary.services.formulary import FormularyService


class PDFGeneratorService:
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form = Form.pdf_generator_.formulary_id_by_company_id_and_form_name(company_id, form_name).first()

    @property
    def field_options_to_use_on_template(self):
        formulary_service = FormularyService(self.user_id, self.company_id)
        form_ids_the_user_has_access_to = formulary_service.formulary_ids_the_user_has_access_to
        fields = Field.pdf_generator_.fields_by_main_form_id_and_company_id(self.form.id, self.company_id)
        field_options = [field for field in fields if field.type.type != 'form']
        for field in fields:
            if field.type.type == 'form' and field.form_field_as_option_id in form_ids_the_user_has_access_to:
                connected_fields = Field.pdf_generator_.fields_by_main_form_id_and_company_id(field.form_field_as_option_id, self.company_id)
                field_options = field_options + [field for field in connected_fields if field.type.type != 'form']
        return field_options