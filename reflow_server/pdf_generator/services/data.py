from reflow_server.pdf_generator.models import PDFTemplateConfigurationVariables


class PDFVariablesData:
    def __init__(self, pdf_template_configuration_id):
        self.__pdf_template_configuration_id = pdf_template_configuration_id
        self.__field_ids = []

    def add_variable(self, field_id):
        self.__field_ids.append(field_id)

    @property   
    def variables(self):
        variables_field_ids = PDFTemplateConfigurationVariables.pdf_generator_.field_ids_by_pdf_template_configuration_id(self.__pdf_template_configuration_id)
        to_add = [field_id for field_id in self.__field_ids if field_id not in variables_field_ids]
        to_exclude = [variable_field_id for variable_field_id in variables_field_ids if variable_field_id not in self.__field_ids]
        return to_add, to_exclude