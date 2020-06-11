from django.conf import settings
from django.db.models import Q

from reflow_server.formula.utils.settings import Structure

import random
import string

class TokenContainer:
    def __init__(self):
        """
        This token container is an object for storing all of the tokens in a single dict.
        As we said earlier, each token should be unique. So we store this here to guarantee it
        is unique and as a single source of truth for each token.
        """
        self.__tokenized = dict()

    def add_token(self, value, token_type, *args, **kwargs):
        """
        Adds a new Token object to __tokenized dict

        Arguments:
            value {str} -- the raw value we want to store, usually as string
            token_type {str} -- the type of the value, could be a number, could be a string an operation, or a field

        Returns:
            str -- a random key that should be updated in the expression.
        """
        key = self.__new_token
        self.__tokenized[key] = Token(value, token_type, *args, **kwargs)
        return key

    def get_token(self, token):
        """
        Retrieves the value of the token. See Token.value for more information on how this works

        Arguments:
            token {str} -- the token that was retrieved when using `.add_token()` function

        Returns:
            str -- the string of the value to be used on the expression. 
        """
        return self.__tokenized[token].value

    @property
    def tokens(self):
        """
        Retrieves all of the tokens saved for the expression.

        Returns:
            list(str) -- list of strings containing all of the tokens saved
        """
        return list(self.__tokenized.keys())

    @property
    def __new_token(self):
        """
        Creates a random and unique key that does not exist in __tokenized dict.

        Returns:
            str -- a random and unique key that represents the value.
        """
        random_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(30))
        while random_key in self.__tokenized:
            random_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(30))
        return random_key


class Token(Structure):
    def __init__(self, value, token_type, *args, **kwargs):
        """
        Tokens are responsible for holding the original value (as raw string) and convert it 
        when the token needs to be used. Instead of converting and making the calculations in real time
        we use tokens as some kind of storage and converter for each value in the expression.

        Arguments:
            value {str} -- the raw value we want to store, usually as string
            token_type {str} -- the type of the value, could be a number, could be a string an operation, or a field

        Keyword Arguments:
            dynamic_form_id {int} -- On `field` token type we want to know, from which formulary data
                                     you want to make the calculation. (default: None)
            is_first_tokenization {bool} -- Usually set to True on the lexer. When we parse a value we convert
                                            the parsed result to a token again, this is set so we can prevent
                                            some inconsistencies that might occur when we tokenize from a lexer 
                                            and from the results of a parser. (default: False)

        Raises:
            ValueError: if the token type is not a valid token type. We accept `number`, `field`, `operation` and `string`,
            other than that we raise a ValueError.
        """
        self.dynamic_form_id = kwargs.get('dynamic_form_id', None)
        self.is_first_tokenization = kwargs.get('is_first_tokenization', False)
        if token_type not in self.types:
            raise ValueError("Must be one of the valid token types, check `reflow_server.formula.utils.settings.Structure`")
        self.type = token_type
        self.__raw_value = value
        self.precision = None

    @property
    def value(self):
        """
        We untokenize the value when we retrieve the data. Usually used in parser.py.

        This is because when data is tokenized it is tokenized as a raw string. When it is
        untokenized we convert each value to what we want, like fields for example.

        Fields works like variables like notifications text. The difference is that here each variable
        is the field id. We use this field id to get the correct value we want to use to make the calculation
        """
        value = str(self.__raw_value)
        if self.type == 'number':
            if self.is_first_tokenization:
                max_precision = settings.DEFAULT_BASE_NUMBER_FIELD_MAX_PRECISION
                value = str(round(float(value.replace('_', '').replace(',','.')), max_precision))
        
        if self.type == 'string':
            if not self.is_first_tokenization:
                value = r"'" + value + r"'"

        if self.type == 'operation':
            value = self.operations[value]
        
        if self.type == 'field':
            from reflow_server.data.models import FormValue

            field_id = value.replace('{{', '').replace('}}', '')
            if self.dynamic_form_id:
                value = FormValue.objects.filter(
                    Q(field_id=int(field_id), form__depends_on_id=self.dynamic_form_id) | 
                    Q(field_id=int(field_id), form_id=self.dynamic_form_id)
                ).values_list('value', flat=True)
                value = ','.join(value)
                if value and not value.lstrip("-").isdigit():
                    value = r"'"+ value +r"'"
                else: 
                    value = str(int(value if value else 0)/settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT)
        return value
