from django.conf import settings

from reflow_server.data.services.representation import RepresentationService
from reflow_server.data.services.formulary.data import FieldValueData
from reflow_server.data.services.formulary.validators import Validator
from reflow_server.data.models import DynamicForm, FormValue
from reflow_server.formulary.services.default_attachment import DefaultAttachmentService

from datetime import datetime, timedelta


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
    
    def __validate_date(self, date_text, date_format=settings.DEFAULT_DATE_FIELD_FORMAT):
        try:
            datetime.strptime(date_text, date_format)
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

        def is_conditional_value_or_parent_conditional_not_valid(section):
            """
            This is a recursive function to validate if the conditional section is NOT valid. To validate we use recursion, this recursion works like
            the following:

            First suppose we have 2 sections, "Motivo da perda" which is conditional, and "Informações de cadastro" and this last one
            has the field "status". On "Motivo da perda" we bound the condition to "status" field, when the value is "perdido", when the value is not "perdido", the condition will not set.

            - We first check if the conditional_on_field field section (aka the Parent section) is a conditional. 
            (on the example above the "conditional_on_field field section" is "Informações de cadastro")
            - Then we check if the conditional of the CURRENT (not the parent) section is validated.
            - IF the PARENT is a conditional and the current section is validated we check the parent section. 
            - We check the parent UNTIL the parent is NOT a conditional or the current section is NOT valid

            - So if the comparison is not checked, we just check if the conditional value IS NOT contained in the field_values of this field. 
            So what we are checking here is that if the section IS NOT (pay attention to the NOT) valid.

            Then just return the boolean value of this comparison.

            Why we use recursion? So we can have a conditional, inside of a conditional, inside of a conditional, with this we can
            validate the hole conditional tree. So, if we have conditionals bounded to the "Motivo da perda" section in the example above,
            and the "status" is not "perda", the conditional sections bounded to "Motivo da perda" will also not be considered when saving.

            Args:
                section (reflow_server.formulary.models.Form): A Form instance where depends_on IS NOT NONE

            Returns:
                bool: Returns True is the section you are veryfying IS NOT valid or False if it is valid.]
            """
            # gets the values that matches the condition_on_field
            is_parent_section_a_conditional_section = section.conditional_on_field.form.conditional_on_field != None
            conditional_value_in_data = [field_value.value for field_value in field_values.get(section.conditional_on_field.id, [])]
            if is_parent_section_a_conditional_section and section.conditional_value in conditional_value_in_data:
                return is_conditional_value_or_parent_conditional_not_valid(section.conditional_on_field.form)
            else:
                return section.conditional_value not in conditional_value_in_data

        for section in self.sections:
            is_conditional_section = section.conditional_on_field != None
            if is_conditional_section:
                # if section is conditional and conditional field has not been inserted 
                is_conditional_name_not_in_section = section.conditional_on_field.id not in field_values.keys()
                # if the conditional is set but the value in the conditional doesn't match the value supplied
                is_conditional_value_not_validated = is_conditional_value_or_parent_conditional_not_valid(section)
                if is_conditional_name_not_in_section or is_conditional_value_not_validated:
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
        cleaned_formulary_data = self.add_formulary_data(formulary_data.uuid, formulary_data.form_data_id)

        for section in formulary_data.get_sections:
            # check if the section is section to be used, check `.__format()` method
            if self.sections.filter(id=section.section_id).exists():
                cleaned_section = cleaned_formulary_data.add_section_data(
                    section.section_id,
                    section.section_uuid,
                    section.section_data_id
                )

                for field in self.fields.filter(form_id=section.section_id):
                    field_values_of_this_field = section.get_field_values_by_field_name(field.name)
                    
                    # We only handle the default value and force it if it's a new formulary data, 
                    # the field_value is not defined and it has default field values
                    # we only check before the clean because of the automatic values
                    is_to_handle_default_field_value = self.default_field_value_by_field_id.get(field.id, None) != None and \
                        len(field_values_of_this_field) == 0 and \
                        self.formulary_data.form_data_id == None

                    # handles default value
                    if is_to_handle_default_field_value:
                        values = self.__handle_default_value(field)
                        for value in values:
                            cleaned_section.add_field_value(field.id, field.name, value)

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

    def __handle_default_value(self, field):
        """
        Force the default field value to be respected if it's not defined. This way the user cannot bypass the default field value.
        The user can bypass this only selecting another value AND NEVER not selecting anything.

        Args:
            field (reflow_server.formulary.models.Field): The Field instance to use

        Returns:
            list(str): A list of string values.
        """
        values = []
        default_field_values = self.default_field_value_by_field_id.get(field.id)
        if field.type.type == 'attachment':
            default_attachment_service = DefaultAttachmentService(self.company_id, self.user_id, field.id)
            # it's kinda dumb to create a draft just to use it next, and it is not performatic, but it guarantee the default
            # field value without many changes to the source code
            for default_field_value in default_field_values:
                draft_string_id = default_attachment_service.get_draft_string_id_from_default_attachment(default_field_value.value, False)
                values.append(draft_string_id)
        else:
            for default_field_value in default_field_values:
                values.append(default_field_value.value)
        return values

    def __dispatch_clean(self, formulary_data, field, field_data):
        """
        Cleans certains types of data recieved, it's important to notice it calls `clean_fieldtype` function
        so you need to be aware of all the possible field_types in order to create another clean function
        """
        handler = getattr(self, '_clean_%s' % field.type.type, None)
        if handler:
            value = handler(formulary_data, field, field_data)
        else:
            value = field_data.value
        
        return value

    def _clean_form(self, formulary_data, field, field_data):
        """
        We need this cleaning because sometimes it will be easier to just match the main_form instead of the section of the
        field directly.
        """
        if field_data.value not in [None, ''] and str(field_data.value).isdigit():
            is_it_matching_to_a_main_form_instead_of_a_section = DynamicForm.objects.filter(id=field_data.value, depends_on_id__isnull=True).exists()
            if is_it_matching_to_a_main_form_instead_of_a_section:
                section_id_to_match = FormValue.objects.filter(form__depends_on_id=field_data.value, field=field.form_field_as_option_id).values_list('form_id', flat=True).first()
                return section_id_to_match
            else:
                return field_data.value
        else:
            return field_data.value

    def _clean_formula(self, formulary_data, field, field_data):
        """
        Similar to `self._clean_id` we use this to bypass the empty value for formulas, this way this value is evaluated after it has been saved.

        Returns:
            str: returns the value of the field or '0' if it doesn't have any value yet.
        """
        value = field_data.value if field_data.value not in [None, ''] and formulary_data.form_data_id else '0'
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
            elif value != '' and not self.__validate_date(value, settings.DEFAULT_DATE_FIELD_FORMAT):
                # we try to format to the value of the field supplied, otherwise we format to the value that was already saved.
                # This can happen if we changed the format of this date field.
                if self.__validate_date(value, field.date_configuration_date_format_type.format):
                    representation = RepresentationService(
                        field.type.type, 
                        field.date_configuration_date_format_type_id, 
                        field.number_configuration_number_format_type_id,
                        field.form_field_as_option_id
                    )
                    value = representation.to_internal_value(value)
                else:
                    try:
                        form_value_instance = FormValue.data_.form_value_by_form_value_id(field_data.field_value_data_id)
                        representation = RepresentationService(
                            form_value_instance.field_type.type, 
                            form_value_instance.date_configuration_date_format_type_id, 
                            form_value_instance.number_configuration_number_format_type_id,
                            field.form_field_as_option_id
                        )
                        value = representation.to_internal_value(value)
                    except:
                        value = ''
        else:
            value = ''
        return value

    
    def _clean_id(self, formulary_data, field, field_data):
        """
        Cleans id from `id` field_type, this just adds a value to the id, so it can pass the checks for empty string.

        Returns:
            str: The new value for the `id` field type
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
            representation = RepresentationService(
                field.type.type, 
                field.date_configuration_date_format_type_id, 
                field.number_configuration_number_format_type_id,
                field.form_field_as_option_id
            )
            value = representation.to_internal_value(value)
        return value
