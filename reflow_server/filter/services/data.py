from django.conf import settings

from datetime import datetime


class FilterConditionData:
    def __init__(self, field, field_type, conditional, is_negation, value, value2='', connector=None): 
        self.conditional = conditional
        self.is_negation = is_negation
        self.field = field
        self.field_type = field_type
        self.value = self.format_value(value)
        self.value2 = self.format_value(value2)
        self.connector = connector
    
    def format_value(self, value):
        if value not in [None, '']:
            if self.field.type.type == 'date':
                return datetime.strptime(value, settings.DEFAULT_DATE_FIELD_FORMAT)
        return value

class FilterFormularyDataData:
    def __init__(self):
        self.formulary_values = {}

    def add_value(self, field_name, field_value):
        self.formulary_values[field_name] = self.formulary_values.get(field_name, []).append(field_value)