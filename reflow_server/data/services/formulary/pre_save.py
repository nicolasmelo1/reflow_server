from django.conf import settings

from reflow_server.data.services.formulary.data import FieldValueData
from reflow_server.data.services.formulary.validators import Validator
from reflow_server.data.models import FormValue

from datetime import datetime, timedelta
import re


class PreSave(Validator):
    """
    Class that format and cleans the formulary data and also extends the
    Validator class to validate the data prior to saving
    """
    def clean_data(self, formulary_data):
        """
        Cleans the data and remove deleted sections and fields.
        """
        self.__format(formulary_data)
        cleaned_formulary_data = self.__clean(formulary_data)
        return cleaned_formulary_data
    
    def __validate_date(self, date_text):
        try:
            datetime.strptime(date_text, settings.DEFAULT_DATE_FIELD_FORMAT)
            return True
        except ValueError:
            return False
    
    def __format(self, formulary_data):
        """
        Formats the values we use for validating specially the fields and sections, we
        don't validate here directly it's just for filtering the querysets and then we can
        use this data for validating if everything matches.

        So in other words, when this class is initialized we get all of the fields and sections
        of the specific formulary. But on here we format those fields and sections with the ones 
        that should be actually used depending of the data that has been sent.

        Okay, but exactly how the conditionals works?
        If you see well we strip out conditional sections when the field has not been filled (in other
        words, there is no data for this field) and the ones whose the value does not match the value 
        in the conditional. 

        Then if you see on `.__clean()` method we create a new formulary data, but this time we only
        append the data from the valid .__sections defined by the `.__format()` method.

        With this architecture we grants 2 things: first, that the conditionals can be validated in the
        field level and that when the conditional is not set we REMOVE the conditional section data
        from our database. (check `reflow_server.formulary.models.abstract.AbstractForm`)
        """
        field_values = formulary_data.get_formatted_fields_data
        section_ids_in_data = [section.section_id for section in formulary_data.get_sections]
        section_ids_to_exclude = []
        
        for section in self.sections:
            conditional_section_is_defined = section.conditional_on_field != None
            if conditional_section_is_defined:
                # if section is conditional and conditional field has not been inserted 
                conditional_name_not_in_section = section.conditional_on_field.id not in field_values.keys()
                # if the conditional is set but the value in the conditional doesn't match the value supplied
                conditional_value_not_validated = section.conditional_value not in [field_value.value for field_value in field_values.get(section.conditional_on_field.id, [])]
                if conditional_name_not_in_section or conditional_value_not_validated:
                    section_ids_to_exclude.append(section.id)
            
            # if the conditional field is not defined but the value is we don't consider it
            elif section.conditional_value not in ['', None]:
                section_ids_to_exclude.append(section.id)

            # if section is a multi-section but it is not in the array of the data, we don't consider it
            # this way we can bypass required fields of multi-sections when they are not added
            if section.type.type == 'multi-form' and section.id not in section_ids_in_data:
                section_ids_to_exclude.append(section.id)
        self.sections = self.sections.exclude(id__in=section_ids_to_exclude)
        self.fields = self.fields.filter(form__id__in=self.sections)
        return None

    def __clean(self, formulary_data):
        """
        Cleanizes the data, remove fields and sections that mustn't be processed.
        
        Not all fields of a section need to be sent in the request, since it is an array of field_values,
        with this, we force to handle the data of this field considering it as empty.
        """
        cleaned_formulary_data = self.add_formulary_data(formulary_data.form_data_id)

        for section in formulary_data.get_sections:
            # check if the section is section to be used, check `.__format()` method
            if self.sections.filter(id=section.section_id).exists():
                cleaned_section = cleaned_formulary_data.add_section_data(
                    section.section_id,
                    section.section_data_id
                )

                for field in self.fields.filter(form_id=section.section_id):
                    field_values_of_this_field = section.get_field_values_by_field_name(field.name)
                    # no values exists for this field on this section
                    if len(field_values_of_this_field) == 0:
                        field_data = FieldValueData(None, field.name, field.id, '')
                        cleaned_value = self.__dispatch_clean(formulary_data, field, field_data)
                        cleaned_section.add_field_value(field.id, field.name, cleaned_value)
                    else:
                        for field_value in field_values_of_this_field:
                            # clean the data
                            cleaned_value = self.__dispatch_clean(formulary_data, field, field_value)
                            cleaned_section.add_field_value(field.id, field.name, cleaned_value, field_value.field_value_data_id)
        
        return cleaned_formulary_data


    def __dispatch_clean(self, formulary_data, field, field_data):
        """
        Cleans certains types of data recieved, it's important to notice it calls `clean_fieldtype` function
        so you need to be aware of all the possible field_types in order to create another clean function
        """
        handler = getattr(self, '_clean_%s' % field.type.type, None)
         # bypass empty value for formulas
        if field.formula_configuration:
            value = '0'
        elif handler:
            value = handler(formulary_data, field, field_data)
        else:
            value = field_data.value
        return value


    def _clean_date(self, formulary_data, field, field_data):
        """
        Cleans date from `date` field_type, this checks arguments in the Field model as `auto_update` or `auto_create`
        Also it is important to notice it converts the date to the DEFAULT_DATE_FIELD_FORMAT defined in `settings.py`.
        Be carefoul overriding  DEFAULT_DATE_FIELD_FORMAT since it can have some serious issues.
        """
        value = field_data.value
        if field.date_configuration_date_format_type:
            if field.date_configuration_auto_create or field.date_configuration_auto_update:
                if field.date_configuration_auto_create and formulary_data.form_data_id and field_data.field_value_data_id:
                    value = FormValue.data_.value_by_form_value_id(field_data.field_value_data_id)
                else:
                    value = datetime.strptime(
                        (
                            datetime.now() + timedelta(hours=self.user.timezone)
                        ).strftime(field.date_configuration_date_format_type.format), field.date_configuration_date_format_type.format
                    ).strftime(settings.DEFAULT_DATE_FIELD_FORMAT)
            elif value != '' and not self.__validate_date(value):
                # we try to format to the value of the field supplied, otherwise we format to the value that was already saved.
                # This can happen if we changed the format of this date field.
                try:
                    value = datetime.strptime(value, field.date_configuration_date_format_type.format).strftime(settings.DEFAULT_DATE_FIELD_FORMAT)
                except:
                    value = datetime.strptime(
                        value, 
                        FormValue.data_.form_value_by_form_value_id(field_data.field_value_data_id).date_configuration_date_format_type.format
                    ).strftime(settings.DEFAULT_DATE_FIELD_FORMAT)
        else:
            value = ''
        return value

    
    def _clean_id(self, formulary_data, field, field_data):
        """
        returns: data

        Cleans id from `id` field_type, this just adds a value to the id, so it can pass the checks for empty string.
        """
        value = field_data.value if field_data.value not in [None, ''] and formulary_data.form_data_id else '0'
        return value


    def _clean_number(self, formulary_data, field, field_data):
        """
        returns: data

        Cleans date from `number` field_type, this checks many arguments in the Field model, especially `number_configuration_number_format_type`
        reference.

        Working with the decimals are a little bit tricky and complicated, we split the decimals from the units in a list then we divide it 
        by the number of characters in it to get 0.decimal_value, round it to the exact precision and multiply by the precision to get an integer
        and lastly add zeroes if it needs to be added, if the decimal is 0, then we need to add a 0 to become 00 if the precision is 100, for other 
        numbers it works as expected.
        """
        value = field_data.value
        if value != '':
            precision = field.number_configuration_number_format_type.precision
            base = field.number_configuration_number_format_type.base

            if field.number_configuration_number_format_type.suffix:
                value = re.sub('(\\{})$'.format(field.number_configuration_number_format_type.suffix), '', value, flags=re.MULTILINE)
            if field.number_configuration_number_format_type.prefix:
                value = re.sub('(^\\{})'.format(field.number_configuration_number_format_type.prefix), '', value, flags=re.MULTILINE)
            if field.number_configuration_number_format_type.decimal_separator:
                value_list = value.split(field.number_configuration_number_format_type.decimal_separator)
                value_list = value_list[:2]

                if len(value_list) > 1:
                    cleaned_decimals = re.sub(r'\D', '',  value_list[1])
                    decimals = int(cleaned_decimals)/int('1' + '0'*len(cleaned_decimals))
                    value_list[1] = str(round(decimals, len(str(precision))-1)).split('.')[1]
                    value_list[1] = value_list[1] + '0'*(len(str(precision))-1 - len(value_list[1]))
                else:
                    value_list.append(str(precision)[1:])
                value = ''.join(value_list)
            negative_signal = value[0]
            value = '{}{}'.format(negative_signal if negative_signal == '-' else '', re.sub(r'\D', '', value))
            value = 0 if value == '' else value
            value = str(int(value)*int(settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT/(precision*base)))
        return value
