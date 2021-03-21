from reflow_server.data.models import FormValue


class Validator:
    """
    Class using for validating the data of a single formulary when saving. First we validate
    the sections if the section data is valid and then we validate each field such as required fields, 
    attachments, and unique fields.
    """
    def formulary_data_is_valid(self, formulary_data):
        """
        Validate required fields respecting the section conditionals,
        if the field is from a conditional section and the conditional is not satisfied, then it's not required.        

        Args:
            formulary_data (reflow_server.formulary.services.formulary.data.FormularyData): 
            the FormularyDataObject with all of the data on the formulary. Including data of sections
            and fields.

        Returns:
            bool: boolean whether a formulary data is valid or not when saving
        """
        self._errors = {}
        
        if not self.__validate_multi_section_and_single_section(formulary_data):
            return False

        if not self.__validate_fields(formulary_data):
            return False

        return True
    
    def __validate_required_field(self, field, field_values):
        if field.type.type != 'id' and field.required:
            if field.id not in field_values or any([field_value.value in [None, ''] for field_value in field_values.get(field.id, [])]):
                self._errors = {'detail': field.name, 'reason': 'required_field', 'data': ''}
                return False
        return True

    def __validate_unique_fields(self, field, field_values):
        if field.is_unique and field.id in field_values: 
            for field_value in field_values[field.id]:
                if field_value.value not in [None, '']:
                    if not field_value.field_value_data_id and FormValue.data_.exists_form_value_by_value_field_id_and_section_id(field_value.value, field.id, field.form_id):
                        self._errors = {'detail': field.name, 'reason': 'already_exists', 'data': field_value.value}
                        return False
                    elif field_value.field_value_data_id and FormValue.data_.exists_form_value_by_value_field_id_and_section_id_excluding_form_value_id(field_value.value, field.id, field.form_id, field_value.field_value_data_id):
                        self._errors = {'detail': field.name, 'reason': 'already_exists', 'data': field_value.value}
                        return False
        return True

    def __validate_multi_section_and_single_section(self, formulary_data):
        section_ids = [section.section_id for section in formulary_data.get_sections if section.section_id and section.section_id != '']
        for section in self.sections:
            # check multiforms, if not a multiform, it should have just one instance of this section
            if section.type.type != 'multi-form' and section_ids.count(section.id) > 1:
                self._errors = {'detail': section.form_name, 'reason': 'just_one_section', 'data': ''}
                return False
        return True
    
    def __validate_fields(self, formulary_data):
        field_values = formulary_data.get_formatted_fields_data
        
        for field in self.fields:
            if not self.__validate_unique_fields(field, field_values):
                return False

            if not self.__validate_required_field(field, field_values):
                return False

        return True

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)
        return self._errors