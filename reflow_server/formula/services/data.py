from reflow_server.formulary.models import Field


class FormulaVariables:
    # ------------------------------------------------------------------------------------------
    class Variable:
        def __init__(self, variable_id):
            field_data = Field.formula_.date_format_id_number_format_id_and_form_field_as_option_id_field_type_by_field_id(variable_id)
            self.variable_id = variable_id
            self.date_format_id = field_data.get('date_configuration_date_format_type_id', None)
            self.number_format_id = field_data.get('number_configuration_number_format_type_id', None)
            self.form_field_as_option_id = field_data.get('form_field_as_option_id', None)
            self.field_type = field_data.get('type__type', None)
    # ------------------------------------------------------------------------------------------
    def __init__(self):
        self.variables = []
    # ------------------------------------------------------------------------------------------
    def add_variable_id(self, variable_id):
        variable = self.Variable(variable_id)
        self.variables.append(variable)


class EvaluationData:
    def __init__(self, status, value):
        self.status = status
        self.value = value


class InternalValue:
    def __init__(self, stringfied_value, value, field_type, number_format_type=None, date_format_type=None):
        self.stringfied_value = stringfied_value
        self.value = value
        self.field_type = field_type
        self.number_format_type = number_format_type
        self.date_format_type = date_format_type
        
        
class IntegrationServiceToAuthenticate:
    def __init__(self, service_name):
        self.service_name = service_name
