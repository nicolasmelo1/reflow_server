class FieldValueData:
    def __init__(self, field_value_data_id, field_name, value):
        self.field_value_data_id = field_value_data_id
        self.field_name = field_name
        self.value = value
        

class SectionData:
    def __init__(self, section_data_id, section_id, formulary_data_id=None):
        self.section_data_id = section_data_id
        self.section_id = section_id
        self.field_values = list()
        self.formulary_data_id = formulary_data_id
    
    def add_field_value(self, field_name, value, field_value_data_id=None):
        # validates if self.formulary_data_id is defined, if it is, it means we are duplicating the value
        # so we ignore the field_value_data_id recievied and set it to None
        field_value_data_id = field_value_data_id if self.formulary_data_id else None

        # we only add values that are not empty strings or none
        if value not in ['', None]:
            field_value_obj = FieldValueData(field_value_data_id, field_name, value)
            self.field_values.append(field_value_obj)
            return field_value_obj
        return None

    @property
    def get_field_values(self):
        return self.field_values


class FormularyData:
    def __init__(self, form_data_id=None):
        self.form_data_id = form_data_id
        self.sections = list()

    def add_section_data(self, section_id, section_data_id=None):
        # validates if self.instance is defined, than we can use the id recieved, otherwise use None
        section_data_id = section_data_id if self.form_data_id else None

        section_data_obj = SectionData(section_data_id, section_id, self.form_data_id)
        self.sections.append(section_data_obj)
        return section_data_obj
    
    @property
    def get_sections(self):
        """
        This function retrieves all of the sections

        Returns:
            list(SectionData): list of SectionData objects
        """
        return self.sections

    @property
    def get_field_values(self):
        """
        This gets all of the field data from all of the sections.

        Returns:
            list(FieldValueData): List of FieldValueData
        """
        return [field_value for section in self.sections for field_value in section.field_values]

    @property
    def get_formatted_fields_data(self):
        """
        Transforms the data here in a way it's easier to validate the fields, basically the following structure:
        >>> { 
            'field_name': [FieldValueData]
            'field_name_2': [FieldValueData, FieldValueData] 
        }
        """
        formatted_field_values = dict()
        for section in self.sections:
            for field_value in section.field_values:
                field_value_item_list = formatted_field_values.get(field_value.field_name, []) 
                field_value_item_list.append(field_value)
                formatted_field_values[field_value.field_name] = field_value_item_list
        return formatted_field_values


class PostSaveData:
    def __init__(self, section_instance, form_value_instance):
        self.section_instance = section_instance
        self.form_value_instance = form_value_instance
