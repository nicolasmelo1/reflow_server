from django.conf import settings
from reflow_server.auth.models import UserExtended
from reflow_server.formulary.models import FormValue
from datetime import datetime
from math import ceil

class RepresentationService:
    def __init__(self, field_type, date_format_type, number_format_type, form_field_as_option, load_ids = False):
        """
        Used for presenting data from this app to the user, everywhere you need to present the data to the user
        so serializers, totals, dashboard and all that stuff.

        Arguments:
            field_type {str} -- str from one of the possible `reflow_server.formulary.models.FieldType`, check the field_type table in our database for reference
            date_format_type {reflow_server.formulary.models.DateFormatType} -- `reflow_server.formulary.models.DateFormatType` model
            number_format_type {reflow_server.formulary.models.NumberFormatType} -- `reflow_server.formulary.models.NumberFormatType` model
            form_field_as_option {reflow_server.formulary.models.Field, reflow_server.theme.models.ThemeField} -- `Field` or `ThemeField` model

        Keyword Arguments:
            load_ids {bool} -- retrieves the ids instead of the value in fields_types like **user** or **form** (default: {False})
        """
        self.field_type = field_type
        self.date_format_type = date_format_type
        self.number_format_type = number_format_type
        self.form_field_as_option = form_field_as_option
        # sometimes i want to retrieve the id instead of the value
        self.load_ids = load_ids

    def representation(self, value):
        if value and value != '':
            handler = getattr(self, 'representation_%s' % self.field_type, None)
            if handler:
                value = handler(value)
        else:
            value = ''
        return value


    def representation_form(self, value):
        try:
            if self.form_field_as_option:
                if not self.load_ids:
                    field_type = self.field_type
                    form_field_as_option_id = self.form_field_as_option.id
                    while field_type == 'form' and value != '' and form_field_as_option_id != '':
                        obj = FormValue.objects.filter(form_id=int(value), field_id=form_field_as_option_id).values('value', 'field_type__type', 'form_field_as_option_id').first()
                        value = obj['value'] if obj else ''
                        field_type = obj['field_type__type'] if obj else None
                        form_field_as_option_id = obj['form_field_as_option_id'] if obj else None
            else:
                value = ''
        except ValueError as ve:
            pass
        return value


    def representation_user(self, value):
        if not self.load_ids:
            value = ' '.join(UserExtended.objects.filter(id=int(value)).values_list('first_name', 'last_name').first())
        return value


    def representation_date(self, value):
        return datetime.strptime(value, settings.DEFAULT_DATE_FIELD_FORMAT).strftime(self.date_format_type.format)
    

    def representation_number(self, value):
        if value.lstrip("-").isdigit() and self.number_format_type:
            negative_signal = value[0] if value[0] == '-' else ''
            value = value.replace('-', '')
            prefix = self.number_format_type.prefix if self.number_format_type.prefix else ''
            suffix = self.number_format_type.suffix if self.number_format_type.suffix else ''
            base = self.number_format_type.base
            thousand_separator = self.number_format_type.thousand_separator if self.number_format_type.thousand_separator else ''
            formater = '{:.' + str(settings.DEFAULT_BASE_NUMBER_FIELD_MAX_PRECISION) + 'f}'
            value = formater.format(float(value)*base/settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT)
            value_and_decimal = value.split('.')
            if self.number_format_type.decimal_separator:
                value_and_decimal[0] = thousand_separator.join([value_and_decimal[0][::-1][i*3:(i*3)+3][::-1] for i in range(ceil(len(value_and_decimal[0])/3))][::-1])
                if len(value_and_decimal)>1:
                    value_and_decimal[1] = value_and_decimal[1][0:len(str(self.number_format_type.precision))-1]
                value = self.number_format_type.decimal_separator.join(value_and_decimal)
            else:
                value = thousand_separator.join([value_and_decimal[0][::-1][i*3:(i*3)+3][::-1] for i in range(ceil(len(value_and_decimal[0])/3))][::-1])
            value = prefix + negative_signal + str(value) + suffix
        return value
