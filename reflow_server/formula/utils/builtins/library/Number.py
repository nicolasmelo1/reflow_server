from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

class Number(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self

    @functionmethod
    def to_round(number, precision=0, **kwargs):
        number = retrieve_representation(number)
        precision = retrieve_representation(precision)

        if isinstance(number, int) or isinstance(number, float) and \
           isinstance(precision, int) or isinstance(precision, float):
            precision = round(precision)
            response = round(number, precision)
            if precision == 0:
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(response)
            else:
                return flow_objects.Float(kwargs['__settings__'])._initialize_(response)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', '`number` and `precision` should be a number')
    
    @functionmethod
    def new(number, **kwargs):
        number = retrieve_representation(number)
    
        if isinstance(number, int) or isinstance(number, float):
            return flow_objects.Float(kwargs['__settings__'])._initialize_(number)
        elif isinstance(number, str):
            try:
                number = float(number)
                return flow_objects.Float(kwargs['__settings__'])._initialize_(number)
            except ValueError as ve:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', '`number` is not a valid number.')
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', '`number` should be a number')

    @functionmethod
    def to_string(number, **kwargs):
        number = retrieve_representation(number)
    
        if isinstance(number, int) or isinstance(number, float):
            return flow_objects.String(kwargs['__settings__'])._initialize_(str(number))
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', '`number` should be a number')

    def _documentation_(self):
        """
        This is the documentation of the formula, this is required because even if we do not translate the formula documentation directly, we need to have
        any default value so users can know what to do and translators can understand how to translate the formula.
        """
        return {
            'description': "This module is responsible for working with numbers inside of Flow. Number is something supposed to work for Floats "
                           "and Integers",
            'methods': {
                'to_round': {
                    'description': "This method is responsible for rounding a number to a certain precision. The precision is a number "
                                   "that is used to round the number to. For example, if we have a number of `1.2345` and we want to round it "
                                   "to `2` decimal places, we would use `to_round(1.2345, 2)`",
                    'attributes': {
                        'number': {
                            'description': "This is the number that we want to round",
                            'is_required': True
                        },
                        'precision': {
                            'description': "This is the precision that we want to round the number to. Defaults to 0.",
                            'is_required': False
                        }
                    }
                },
                'new': {
                    'description': "This method is responsible for creating a new number. The number can be either an Integer or a Float.",
                    'attributes': {
                        'number': {
                            'description': "This is the number that we want to create",
                            'is_required': True
                        }
                    }
                },
                'to_string': {
                    'description': "This method is responsible for converting a number to a string.",
                    'attributes': {
                        'number': {
                            'description': "This is the number that we want to convert to a string",
                            'is_required': True
                        }
                    }
                }
            }
        }