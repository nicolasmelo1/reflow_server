from django.conf import settings

from reflow_server.formula.exceptions import FormulaException
from reflow_server.formula.utils.parser import Parser

class FormulaService:
    def __init__(self, expression, *args, **kwargs):
        """
        Recieves the raw formula as a raw string and calculates it when the user tries to
        retrieve the value using `.value`

        Arguments:
            expression {str} -- the formula effectively, it's just a raw formula, could be as simple as
                                1+1 or more complex like SUM( 2 + 2 ; COUNT("A", 2 , 3 ))
        Keyword Arguments:
            precision {int} -- The max precision to recieve the value, follow the precision defined in 
                               FieldNumberFormatType, so if you want precision of 2, use 100, if you want precision
                               of 3, use 1000 and so on.
            dynamic_form_id {int} -- On `field` token type we want to know, from which formulary data
                                     you want to make the calculation. (default: None)
            is_first_tokenization {bool} -- Usually set to True on the lexer. When we parse a value we convert
                                            the parsed result to a token again, this is set so we can prevent
                                            some inconsistencies that might occur when we tokenize from a lexer 
                                            and from the results of a parser. (default: False)
        """
        self.precision = kwargs.get('precision', None)
        try:
            self.__parser = Parser(expression, *args, **kwargs)
        except FormulaException as fe:
            pass

    @property
    def value(self):
        """
        Gets the value of the formula, it's important to understand that for numbers, inside of python
        the numbers need to be normalized, so instead of the number multiplied by DEFAULT_BASE_NUMBER_FIELD_FORMAT
        we calculate as the default number. even floats. After the result, we convert the number back to
        the DEFAULT_BASE_NUMBER_FIELD_FORMAT. This way we can seamlessly work between python numbers
        and reflow default base numbers.

        Also it's important to understand that the formulas might not be valid sometime, so we always give
        the result, even if an exception was thrown (like Excel sheets). We use #Error for attribute errors
        and #N/A for all the other possible errors. Like when the CPU is bombarded with bound heavy calculations.
        """
        try:
            result = self.__parser.parse()
            if type(result) in [int, float]:
                max_precision = settings.DEFAULT_BASE_NUMBER_FIELD_MAX_PRECISION if not self.precision else len(str(self.precision))-1
                splitted_value = str(round(result,max_precision)).split('.')
                length_of_value_decimals = len(splitted_value[1]) if len(splitted_value) > 1 else 0
                num_of_zeroes = settings.DEFAULT_BASE_NUMBER_FIELD_MAX_PRECISION - length_of_value_decimals
                zeroes = '0'*num_of_zeroes
                return int((''.join(splitted_value)+zeroes))
            else:
                return result
        except AttributeError as ae:
            return '#ERROR'
        except Exception as e:
            return '#N/A'