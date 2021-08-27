from django.conf import settings

from datetime import datetime

def format_value(field_type, value):
    if value not in [None, '']:
        if field_type == 'date':
            return datetime.strptime(value, settings.DEFAULT_DATE_FIELD_FORMAT)
        elif field_type == 'number':
            return int(value)
    return value


class FilterConditionData:
    def __init__(self, field, field_type, conditional, is_negation, value, value2='', connector=None): 
        self.conditional = conditional
        self.is_negation = is_negation
        self.field = field
        self.field_type = field_type
        self.value = format_value(field_type, value)
        self.value2 = format_value(field_type, value2)
        self.connector = connector
    

class FilterFormularyDataData:
    def __init__(self):
        """
        I know the name looks like a misstype of the name of the class but it's not. The FormularyData means that we will use
        this as a helper to hold all of the data of a formulary. So we are dealing with the data/record of the formulary and not the actual
        Formulary itself. The last Data means this is a helper for the services to handle the data needed for the services.
        """
        self.formulary_values = {}

    def add_value(self, field_type, field_name, field_value):
        self.formulary_values[field_name] = self.formulary_values.get(field_name, [])
        self.formulary_values[field_name].append(
            format_value(field_type, field_value)
        )