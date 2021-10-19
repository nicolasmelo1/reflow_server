from django.conf import settings

from reflow_server.data.models import FormValue
from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.models import FieldNumberFormatType, FieldDateFormatType

from datetime import datetime
import decimal
import re

representation_date_format_type_cache = {}
representation_number_format_type_cache = {}

class RepresentationDateFormatTypeData:
    """
    By making this we don't need to make queries everytime we want to use a FieldDateFormatType instance. This
    guarantees no query is made and we can cache it
    """
    def __init__(self, format_type_name, date_format):
        self.format_type_name = format_type_name
        self.format = date_format

class RepresentationNumberFormatTypeData:
    """
    By making this we don't need to make queries everytime we want to use a FieldNumberFormatType instance. This
    guarantees no query is made and we can cache it
    """
    def __init__(self, format_type_name, precision, prefix, suffix, thousand_separator, decimal_separator, base, has_to_enforce_decimal=False):
        self.format_type_name = format_type_name
        self.precision = precision
        self.prefix = prefix
        self.suffix = suffix
        self.thousand_separator = thousand_separator
        self.decimal_separator = decimal_separator
        self.base = base
        self.has_to_enforce_decimal = has_to_enforce_decimal

class RepresentationService:
    def __init__(self, field_type, date_format_type_id, number_format_type_id, form_field_as_option_id, load_ids = False):
        """
        Used for presenting data from this app to the user, use it everywhere you need to present the data 
        from the backend to the normal user. So use this in serializers, dashboard, totals and etc.

        Dates for example, change the formatting, to the formatting that the user set.
        Numbers are divided by the DEFAULT_BASE_NUMBER_FIELD_FORMAT with the precision.
        Users are represented as `first_name` + `last_name`
        Connection is not the ID of the formulary but the data of the field it connects to.
        
        And so on...

        Exposes `.representation()` function and `.to_internal_value()` function

        Args:
            field_type (str): from one of the possible `field_types`, check the `field_type` table in our database for reference
            date_format_type_id (int): The FieldDateFormatType instance id that the field uses
            number_format_type_id (int): The FieldNumberFormatType instance id that the field uses
                                                                                       to format the base number to the desired format
            form_field_as_option_id (int): The Field or ThemeField instance id of the connected field
            load_ids (bool, optional): retrieves the ids instead of the value in fields_types like `user` or `form`. Defaults to False.
        """
        # making this we don't need to make queries every time date_format_type
        representation_number_format_type = None
        representation_date_format_type = None
        if date_format_type_id:
            if representation_date_format_type_cache.get(date_format_type_id, None):
                representation_date_format_type = representation_date_format_type_cache[date_format_type_id]
            else:
                date_format_type = FieldDateFormatType.objects.filter(id=date_format_type_id).first()
                representation_date_format_type_cache[date_format_type_id] = RepresentationDateFormatTypeData(
                    date_format_type.type, date_format_type.format
                )
                representation_date_format_type = representation_date_format_type_cache[date_format_type_id]

        # making this we don't need to make queries every time to retrieve a number_format_type
        if number_format_type_id:
            if representation_number_format_type_cache.get(number_format_type_id, None):
                representation_number_format_type = representation_number_format_type_cache[number_format_type_id]
            else:
                number_format_type = FieldNumberFormatType.objects.filter(id=number_format_type_id).first()

                representation_number_format_type_cache[number_format_type_id] = RepresentationNumberFormatTypeData(
                    number_format_type.type, 
                    number_format_type.precision,
                    number_format_type.prefix,
                    number_format_type.suffix,
                    number_format_type.thousand_separator,
                    number_format_type.decimal_separator,
                    number_format_type.base,
                    number_format_type.has_to_enforce_decimal
                )
                representation_number_format_type = representation_number_format_type_cache[number_format_type_id]
        

        self.field_type = field_type
        self.date_format_type = representation_date_format_type
        self.number_format_type = representation_number_format_type
        self.form_field_as_option_id = form_field_as_option_id
        # sometimes i want to retrieve the id instead of the value
        self.load_ids = load_ids

    def to_internal_value(self, value):
        """
        As `.representation` is used when retrieving the value for the user this is used when retrieving the value FROM the user.
        So this converts the value that the user inputs to the value that we use internally.

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

        Args:
            value (str): The value you want to format

        Returns:
            str: The value formatted
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

        Because of this, this function is recursive, so we can format the value of the connected field.
        """
        try:
            if self.form_field_as_option_id:
                if not self.load_ids and value != '' and self.form_field_as_option_id:
                    # we get all of the form_values that match the condition, we match the formulary
                    # not the section, this means that sometimes the section is multi_form, so we have multiple
                    # fields matching the connection, so in order to display the value right we get all of the values it should connect to.
                    form_values_connected = FormValue.data_.form_value_by_form_id_and_field_id(
                        int(value), 
                        self.form_field_as_option_id
                    )
                    if form_values_connected:
                        values_to_display = []
                        for form_value_connected in form_values_connected:
                            representation_service = self.__class__(
                                form_value_connected.field_type,
                                form_value_connected.date_configuration_date_format_type_id,
                                form_value_connected.number_configuration_number_format_type_id,
                                form_value_connected.form_field_as_option_id,
                                self.load_ids
                            )
                            values_to_display.append(representation_service.representation(form_value_connected.value))
                        return ' | '.join(values_to_display)
                    else:
                        value = ''
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
        try:
            return datetime.strptime(value, settings.DEFAULT_DATE_FIELD_FORMAT).strftime(self.date_format_type.format)
        except ValueError as ve:
            return value
    
    def _representation_number(self, value):
        if value.lstrip("-").isdigit() and self.number_format_type:
            negative_signal = value[0] if value[0] == '-' else ''
            value = value.replace('-', '')
            prefix = self.number_format_type.prefix if self.number_format_type.prefix else ''
            suffix = self.number_format_type.suffix if self.number_format_type.suffix else ''
            base = self.number_format_type.base
            thousand_separator = self.number_format_type.thousand_separator if self.number_format_type.thousand_separator else ''

            value = decimal.Decimal(str(value))*decimal.Decimal(str(base))/decimal.Decimal(str(settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT))
            # work on the decimal part
            if self.number_format_type.decimal_separator:
                formater = '{:.0f}'
                if self.number_format_type.has_to_enforce_decimal:
                    formater = '{:.' + str(len(str(self.number_format_type.precision))-1) + 'f}'
                else:
                    value_and_decimal_splitted = str(value).split('.')
                    if len(value_and_decimal_splitted) > 1:
                        decimal_of_value = str(value_and_decimal_splitted[1])
                        formater = '{:.' + str(len(decimal_of_value)) + 'f}'
                value = str(formater).format(value)
                value = value.replace('.', self.number_format_type.decimal_separator)
            value_and_decimal = str(value).split(self.number_format_type.decimal_separator)
            if thousand_separator != '':
                # reference: https://stackoverflow.com/questions/1823058/how-to-print-number-with-commas-as-thousands-separators
                value_and_decimal[0] = '{:,}'.format(int(value_and_decimal[0]))
                value_and_decimal[0] = value_and_decimal[0].replace(',', thousand_separator)
                value = self.number_format_type.decimal_separator.join(value_and_decimal)
            value = prefix + negative_signal + str(value) + suffix
        return value
