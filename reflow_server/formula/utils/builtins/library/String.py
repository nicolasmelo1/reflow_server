from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    LibraryStruct, retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects


class String(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self
    
    @functionmethod
    def extract(text, first_character=0, number_of_characters=1, **kwargs):
        text = retrieve_representation(text)
        first_character = retrieve_representation(first_character)
        number_of_characters = retrieve_representation(number_of_characters)

        is_text_a_string = isinstance(text, str)
        is_first_character_a_number = isinstance(first_character, int) or isinstance(first_character, float)
        is_number_of_characters_a_number = isinstance(number_of_characters, int) or isinstance(number_of_characters, float)
        if (is_text_a_string and is_first_character_a_number and is_number_of_characters_a_number):
            extracted_string = text[first_character:first_character + number_of_characters]
            return flow_objects.String(kwargs['__settings__'])._initialize_(extracted_string)
        else:
            if not is_text_a_string:
                flow_objects.Error(kwargs['__settings__'])._initialize_('StringError', '`text` should be a string.')
            if not is_first_character_a_number:
                flow_objects.Error(kwargs['__settings__'])._initialize_('StringError', "`first_character` should be a number. It's the position we start counting.")
            if not is_number_of_characters_a_number:
                flow_objects.Error(kwargs['__settings__'])._initialize_('StringError', "`number_of_characters` should be a number. It's the number of characters we want to extract.")

    def _documentation_(self):
        return {
            "description": "Module responsible for doing stuff with strings, this is responsible for things like extracting substrings, converting to a new "
                           "string and so on.",
            "methods": {
                "extract": {
                    'description': "Extracts a substring from a text, works in a similar fashion like Excel's `EXT.STRING`, the first "
                                   "character starts from 1 and counts up as many characters as you want.",
                    'attributes': {
                        'text': {
                            'description': "The text from which we want to extract a substring.",
                            'is_required': True
                        },
                        'first_character': {
                            'description': "The first character we want to start counting from. Defaults to 0",
                            'is_required': False
                        },
                        'number_of_characters': {
                            'description': "The number of characters you want to extract from the string",
                            'is_required': False
                        },
                    }
                }
            }
        }