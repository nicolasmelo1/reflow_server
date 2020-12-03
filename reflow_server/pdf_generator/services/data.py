class PDFVariableData:
    def __init__(self, variable_id, field_id):
        self.variable_id = variable_id
        self.field_id = field_id


class PDFVariablesData:
    def __init__(self):
        self.variables = []

    def add_variable(self, variable_id, field_id):
        pdf_variable = PDFVariableData(variable_id, field_id)
        self.variables.append(pdf_variable)
        return pdf_variable