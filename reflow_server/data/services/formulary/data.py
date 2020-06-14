class FieldValueData:
    def __init__(self, field_value_data_id, field_name, value):
        self.field_value_data_id = field_value_data_id
        self.field_name = field_name
        self.value = value
        

class SectionData:
    def __init__(self, section_data_id, section_id, formulary_data_id=None):
        self.section_data_id = section_data_id
        self.section_id = section_id
        self.__field_values = list()
        self.formulary_data_id = formulary_data_id
    
    def add_field_value(self, field_name, value, field_value_data_id=None):
        """
        This function is used to add field_values to sections. remember that formularies is a conjunction of sections following
        a conjuction of fields. This function is a handy function to add field_values to the section data with a new object.
        This way we are not bounded to serializers and that kind of stuff. 

        Args:
            field_name (str): Each value is from a field, from which field does is the value from?
            value (str): It doesn't matter if it is a number, date or any kind, we need ALWAYS a string
            field_value_data_id (int, optional): Are you editing a value that already existis in the database or adding a new one?
                                                 If you are editing we need the FormValue.id in order to work with this data. Defaults to None.

        Returns:
            None: Just a default return statement but is not needed for anything
        """
        # validates if self.formulary_data_id is defined, if it is, it means we are duplicating the value
        # so we ignore the field_value_data_id recievied and set it to None
        field_value_data_id = field_value_data_id if self.formulary_data_id else None

        # we only add values that are not empty strings or none
        if value not in ['', None]:
            field_value_obj = FieldValueData(field_value_data_id, field_name, value)
            self.__field_values.append(field_value_obj)
            return field_value_obj
        return None
    
    def get_field_values_by_field_name(self, field_name):
        """
        Gets the values of a field on this particular section from a specific `field_name`

        Args:
            field_name (str): The name of the field

        Returns:
            list(FieldValueData): List of FieldValues from this section
        """
        return [field for field in self.__field_values if field_name == field.field_name]

    @property
    def get_field_values(self):
        """
        Gets all of the field_values of this object, we use this so the user don't have access to the data directly. It means
        the user can't append any new data to the fields without using the function `.add_field_value()` provided to add new field_values data

        Returns:
            list(FieldValueData): List of FieldValues from this section
        """
        return self.__field_values


class FormularyData:
    def __init__(self, form_data_id=None):
        self.form_data_id = form_data_id
        self.__sections = list()

    def add_section_data(self, section_id, section_data_id=None):
        # validates if self.instance is defined, than we can use the id recieved, otherwise use None
        section_data_id = section_data_id if self.form_data_id else None

        section_data_obj = SectionData(section_data_id, section_id, self.form_data_id)
        self.__sections.append(section_data_obj)
        return section_data_obj
    
    @property
    def get_sections(self):
        """
        This function retrieves all of the sections

        Returns:
            list(SectionData): list of SectionData objects
        """
        return self.__sections

    @property
    def get_field_values(self):
        """
        This gets all of the field data from all of the sections.

        Returns:
            list(FieldValueData): List of FieldValueData
        """
        return [field_value for section in self.__sections for field_value in section.get_field_values]

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
        for section in self.__sections:
            for field_value in section.get_field_values:
                field_value_item_list = formatted_field_values.get(field_value.field_name, []) 
                field_value_item_list.append(field_value)
                formatted_field_values[field_value.field_name] = field_value_item_list
        return formatted_field_values


class PostSaveData:
    def __init__(self, section_instance, form_value_instance):
        self.section_instance = section_instance
        self.form_value_instance = form_value_instance
