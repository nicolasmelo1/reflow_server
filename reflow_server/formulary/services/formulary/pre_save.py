from reflow_server.formulary.models import Form, Field

from datetime import datetime, timedelta
import re


class PreSave:
    def __init__(self):
        self.__sections = Form.objects.filter(
            depends_on__form_name= self.__form_name, 
            depends_on__group__company_id=self.__company_id, 
            enabled=True
        )
        self.__fields = Field.objects.filter(
            form__depends_on__form_name= self.__form_name,
            form__id__in=self.__sections,
            form__enabled=True,
            enabled=True
        )
        self.__field_values = self.formulary_data.get_formatted_fields_data
        self.__format()

    def __append_new_form_value(self, field, data):
        """
        Adds an empty value if necessary in order to be pre or post processed

        return data
        """
        if field.date_configuration_auto_create or field.date_configuration_auto_update or field.type.type == 'id' or field.formula_configuration not in ('', None):
            data.append({'id': None, 'value': '', 'field_name': field.name})
        
        return data

    def __format(self):
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
        section_ids_to_exclude = []
        for section in self.__sections:
            # if section is conditional and conditional field has not been inserted we exclude this section
            if section.conditional_on_field and \
               section.conditional_on_field.name not in self.field_values.keys():
                section_ids_to_exclude.append(section.id)
            # if the conditional is set but the value in the conditional doesn't match the value supplied
            elif section.conditional_on_field and \
                 section.conditional_value not in [field_value.value for field_value in self.field_values[section.conditional_on_field.name]]:
                section_ids_to_exclude.append(section.id)
        
        self.__sections = self.__sections.exclude(id__in=section_ids_to_exclude)
        self.__fields = self.__fields.filter(form__id__in=self.__sections)
        

    def __clean(self):
        """
        Cleanizes the data, remove fields and sections that mustn't be processed.
        
        Not all fields of a section need to be sent in the request, since it is an array of field_values,
        with this, we force to handle the data of this field considering it as empty.
        """
        validated_data = self.add_formulary_data(self.formulary_data.form_data_id)

        for section in self.formulary_data:
            # check if the section is section to be used, check `.__format()` method
            if self.__sections.filter(id=section.section_id).exists():
                validated_section = validated_data.add_section_data(
                    section.section_id,
                    section.section_data_id
                )

                for field in self.__fields.filter(form_id=section.section_id):
                    if field.name not in self.__field_values:
                        field_form_values = self.__append_new_form_value(field, field_form_values)
                    else:
                        for field_values in field_form_values:
                            # clean the data
                            fields_values = self.__dispatch_clean(field, field_values)
                            validated_section['dynamic_form_value'].append(field_values)    


    def __dispatch_clean(self, field, data):
        """
        Cleans certains types of data recieved, it's important to notice it calls `clean_fieldtype` function
        so you need to be aware of all the possible field_types in order to create another clean function
        """
        handler = getattr(self, 'clean_%s' % field.type.type, None)
        if handler:
            data = handler(field, data)

        return data


    def clean_date(self, field, data):
        """
        returns: data

        Cleans date from `date` field_type, this checks arguments in the Field model as `auto_update` or `auto_create`
        Also it is important to notice it converts the date to the DEFAULT_DATE_FIELD_FORMAT defined in `settings.py`.
        Be carefoul overriding  DEFAULT_DATE_FIELD_FORMAT since it can have some serious issues.
        """
        if field.date_configuration_auto_create or field.date_configuration_auto_update:
            if field.date_configuration_auto_create and self.__instance and data['id']:
                data['value'] = FormValue.objects.filter(id=data['id']).values_list('value', flat=True).first()
            else:
                data['value'] = datetime.strptime(
                    (datetime.now() + timedelta(hours=self.__user.timezone)).strftime(field.date_configuration_date_format_type.format),
                    field.date_configuration_date_format_type.format
                    ).strftime(DEFAULT_DATE_FIELD_FORMAT)
        elif data['value'] != '' and not validate_date(data['value']):
            # we try to format to the value of the field, otherwise we format to the value that was already saved.
            try:
                data['value'] = datetime.strptime(data['value'], field.date_configuration_date_format_type.format).strftime(DEFAULT_DATE_FIELD_FORMAT)
            except:
                data['value'] = datetime.strptime(
                    data['value'], 
                    FormValue.objects.filter(id=data['id']).first().date_configuration_date_format_type.format
                ).strftime(DEFAULT_DATE_FIELD_FORMAT)
        return data

    
    def clean_id(self, field, data):
        """
        returns: data

        Cleans id from `id` field_type, this just adds a value to the id, so it can pass the checks for empty string.
        """
        data['value'] = data['value'] if 'value' in data and data['value'] not in [None, ''] and self.__instance else '0'
        return data


    def clean_number(self, field, data):
        """
        returns: data

        Cleans date from `number` field_type, this checks many arguments in the Field model, especially `number_configuration_number_format_type`
        reference.

        Working with the decimals are a little bit tricky and complicated, we split the decimals from the units in a list then we divide it 
        by the number of characters in it to get 0.decimal_value, round it to the exact precision and multiply by the precision to get an integer
        and lastly add zeroes if it needs to be added, if the decimal is 0, then we need to add a 0 to become 00 if the precision is 100, for other 
        numbers it works as expected.
        """
        if data['value'] != '':
            precision = field.number_configuration_number_format_type.precision
            base = field.number_configuration_number_format_type.base

            if field.number_configuration_number_format_type.suffix:
                data['value'] = re.sub('(\\{})$'.format(field.number_configuration_number_format_type.suffix), '', data['value'], flags=re.MULTILINE)
            if field.number_configuration_number_format_type.prefix:
                data['value'] = re.sub('(^\\{})'.format(field.number_configuration_number_format_type.prefix), '', data['value'], flags=re.MULTILINE)
            if field.number_configuration_number_format_type.decimal_separator:
                value_list = data['value'].split(field.number_configuration_number_format_type.decimal_separator)
                value_list = value_list[:2]

                if len(value_list) > 1:
                    cleaned_decimals = re.sub(r'\D', '',  value_list[1])
                    decimals = int(cleaned_decimals)/int('1' + '0'*len(cleaned_decimals))
                    value_list[1] = str(round(decimals, len(str(precision))-1)).split('.')[1]
                    value_list[1] = value_list[1] + '0'*(len(str(precision))-1 - len(value_list[1]))
                else:
                    value_list.append(str(precision)[1:])
                data['value'] = ''.join(value_list)
            negative_signal = data['value'][0]
            data['value'] = '{}{}'.format(negative_signal if negative_signal == '-' else '', re.sub(r'\D', '', data['value']))
            data['value'] = 0 if data['value'] == '' else data['value']            
            data['value'] = str(int(data['value'])*int(DEFAULT_BASE_NUMBER_FIELD_FORMAT/(precision*base)))

        return data

    def is_valid(self):
        """
        Validate required fields respecting the section conditionals,
        if the field is from a conditional section and the conditional is not satisfied, then it's not required.

        :return: True or False
        """
        self._errors = {}

        field_value = self.__reformat_data()
        
        # validate sections
        section_ids = [sections['form_id'] for sections in self.__data['depends_on_dynamic_form']]
        for section in self.__sections:
            # check multiforms, if not a multiform, it should have just one instance of this section
            if section.type.type != 'multi-form' and [sections['form_id'] for sections in self.__data['depends_on_dynamic_form']].count(section.id) > 1:
                self._errors = {'detail': section.form_name, 'reason': 'just_one_section', 'data': ''}
                return False

        # validate fields
        for field in self.__fields:
            # check unique fields
            if field.is_unique and field.name in field_value: 
                for field_values in field_value[field.name]:
                    if field_values['value'] not in [None, '']:
                        if not field_values['id'] and FormValue.objects.filter(value=field_values['value'], field=field, form__form_id=field.form_id).exists():
                            self._errors = {'detail': field.name, 'reason': 'already_exists', 'data': field_values['value']}
                            return False
                        elif field_values['id'] and FormValue.objects.filter(value=field_values['value'],field=field, form__form_id=field.form_id).exclude(id=field_values['id']).exists():
                            self._errors = {'detail': field.name, 'reason': 'already_exists', 'data': field_values['value']}
                            return False

            # check attachments
            if field.type.type == 'attachment' and field.name in field_value:
                for field_values in field_value[field.name]:
                    attachment_file_format = field_values['value'].split('.').pop()
                    if field_values['value'] != '' and attachment_file_format.lower() not in ['doc','docx', 'jpeg', 'jpg', 'pdf', 'png',
                    'wav', 'xls', 'xlsx', 'zip']:
                        self._errors = {'detail': field.name, 'reason': 'invalid_file', 'data': field_values['value']}
                        return False

            # check required
            if field.type.type != 'id' and field.required:
                if field.name not in field_value or any([not value.get('value', None) or value['value'] == '' for value in field_value.get(field.name, [])]):
                    self._errors = {'detail': field.name, 'reason': 'required_field', 'data': ''}
                    return False

        return True

    def __remove_deleted(self):
        """
        Checks if anything has been deleted, and deletes it.

        Only works if instance is set in the serializer class, since it means you are trying to update a model,
        otherwise, nothing is made and we ignore this function.
        """
        if len(self.__data) != 0 and self.__instance:
            bucket = Bucket()

            section_ids = [int(depends_on_dyamic_form['id']) for depends_on_dyamic_form in self.__data.get('depends_on_dynamic_form') if depends_on_dyamic_form.get('id', None) and depends_on_dyamic_form['id'] != '']
            form_value_ids = [int(value['id']) for section in self.__data.get('depends_on_dynamic_form') for value in section.get('dynamic_form_value') if value.get('id', None) and value['id'] != '']
            
            fields = Field.objects.filter(form__depends_on__form_name=self.__form_name)
            disabled_fields = fields.filter(Q(enabled=False) | Q(form__enabled=False)).values('id', 'form_id')

            form_value_to_delete = FormValue.objects.filter(form__depends_on=self.__instance).exclude(Q(id__in=form_value_ids) | Q(field_id__in=[disabled_field['id'] for disabled_field in disabled_fields]))
            dynamic_forms_to_delete = DynamicForm.objects.filter(form__enabled=True, depends_on=self.__instance).exclude(id__in=section_ids)
            
            # remove attachments from s3
            for attachment_value in form_value_to_delete.filter(field_type__type='attachment'):
                attachment_to_delete = Attachments.objects.filter(form=attachment_value.form, file=attachment_value.value, field=attachment_value.field).first()
                if attachment_to_delete:
                    bucket.delete(key="{file_attachments_path}/{id}/{field}/{file}".format(
                                        id=str(attachment_to_delete.pk),
                                        field=str(attachment_to_delete.field.pk),
                                        file=str(attachment_to_delete.file),
                                        file_attachments_path=S3_FILE_ATTACHMENTS_PATH))
                    attachment_to_delete.delete()
            form_value_to_delete.delete()
            dynamic_forms_to_delete.delete()

    @property
    def errors(self):
        if not hasattr(self, '_errors'):
            msg = 'You must call `.is_valid()` before accessing `.errors`.'
            raise AssertionError(msg)
        return self._errors