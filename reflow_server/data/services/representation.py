from django.conf import settings

from reflow_server.data.models import FormValue
from reflow_server.authentication.models import UserExtended

from datetime import datetime
from math import ceil
import decimal
import re


class RepresentationService:
    def __init__(self, field_type, date_format_type, number_format_type, form_field_as_option, load_ids = False):
        """
        Used for presenting data from this app to the user, use it everywhere you need to present the data 
        from the backend to the normal user. So use this in serializers, dashboard, totals and etc.

        Dates for example, change the formatting, to the formatting that the user set.
        Numbers are divided by the DEFAULT_BASE_NUMBER_FIELD_FORMAT with the precision.
        Users are represented as `first_name` + `last_name`
        Connection is not the ID of the formulary but the data of the field it connects to.
        
        And so on...

        Exposes `.representation()` function

        Arguments:
            field_type {str} -- from one of the possible `field_types`, check the `field_type` table in our database for reference
            date_format_type {reflow_server.models.formulary.FieldDateFormatType} -- The date format of the field, we use this for formatting
            number_format_type {reflow_server.models.formulary.FieldNumberFormatType} -- The number format type, so we can format it correctly
            form_field_as_option {reflow_server.models.formulary.Field / reflow_server.models.theme.ThemeField} -- The field model effectively

        Keyword Arguments:
            load_ids {bool} -- retrieves the ids instead of the value in fields_types like `user` or `form` (default: {False})
        """
        self.field_type = field_type
        self.date_format_type = date_format_type
        self.number_format_type = number_format_type
        self.form_field_as_option = form_field_as_option
        # sometimes i want to retrieve the id instead of the value
        self.load_ids = load_ids

    def to_internal_value(self, value):
        """
        As `.representation` is used when retrieving the value for the user this is used when retrieving the value from the user.
        So this is the value we use internally.

        Args:
            value (str): The value you are recieving

        Returns:
            str: The value formated and ready to be saved in the database
        """
        if value and value != '':
            handler = getattr(self, '_to_internal_value_%s' % self.field_type, None)
            if handler:
                value = handler(value)
        else:
            value = ''
        return value

    def _to_internal_value_date(self, value):
        return datetime.strptime(value, self.date_format_type.format).strftime(settings.DEFAULT_DATE_FIELD_FORMAT)
    
    def _to_internal_value_number(self, value):
        precision = self.number_format_type.precision
        base = self.number_format_type.base

        if self.number_format_type.suffix:
            value = re.sub('(\\{})$'.format(self.number_format_type.suffix), '', value, flags=re.MULTILINE)
        if self.number_format_type.prefix:
            value = re.sub('(^\\{})'.format(self.number_format_type.prefix), '', value, flags=re.MULTILINE)
        if self.number_format_type.decimal_separator:
            value_list = value.split(self.number_format_type.decimal_separator)
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
        
    def representation(self, value):
        """
        This effectively recieves a value and transforms it to an human readable value.

        Arguments:
            value {str} -- The value you want to format

        Returns:
            str -- The value formatted
        """
        if value and value != '':
            handler = getattr(self, '_representation_%s' % self.field_type, None)
            if handler:
                value = handler(value)
        else:
            value = ''
        return value


    def _representation_form(self, value):
        """
        This seems inneficient, it's because it is. But it needs to be done this way. 
        We can have a "form" value pointing to another "form" value and so on. We need to
        get the furtherst reference to the value. If the user don't want to we don't have 
        to return the id of this reference.
        """
        try:
            if self.form_field_as_option:
                if not self.load_ids and value != '' and self.form_field_as_option.id:
                    obj = FormValue.data_.form_value_by_form_id_and_field_id(form_id=int(value), field_id=self.form_field_as_option.id)
                    representation_service = self.__class__(
                        obj.field_type,
                        obj.date_configuration_date_format_type,
                        obj.number_configuration_number_format_type,
                        obj.form_field_as_option,
                        self.load_ids
                    )
                    value = representation_service.representation(obj.value)
            else:
                value = ''
        except ValueError as ve:
            pass
        return value


    def _representation_user(self, value):
        if not self.load_ids:
            value = UserExtended.data_.user_full_name_by_user_id(int(value))
        return value


    def _representation_date(self, value):
        return datetime.strptime(value, settings.DEFAULT_DATE_FIELD_FORMAT).strftime(self.date_format_type.format)
    

    def _representation_number(self, value):
        if value.lstrip("-").isdigit() and self.number_format_type:
            negative_signal = value[0] if value[0] == '-' else ''
            value = value.replace('-', '')
            prefix = self.number_format_type.prefix if self.number_format_type.prefix else ''
            suffix = self.number_format_type.suffix if self.number_format_type.suffix else ''
            base = self.number_format_type.base
            thousand_separator = self.number_format_type.thousand_separator if self.number_format_type.thousand_separator else ''
            formater = '{:.' + str(settings.DEFAULT_BASE_NUMBER_FIELD_MAX_PRECISION) + 'f}'
            
            value = formater.format((decimal.Decimal(str(value))*decimal.Decimal(str(base))/decimal.Decimal(str(settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT))))
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
