
from reflow_server.formula.utils.helpers import DatetimeHelper
from reflow_server.formula.utils.context import Context

import re


class TokenType:
    ASSIGN='ASSIGN'
    INTEGER='INTEGER'
    FLOAT='FLOAT'
    BOOLEAN='BOOLEAN'
    DATETIME='DATETIME'
    POSITIONAL_ARGUMENT_SEPARATOR='POSITIONAL_ARGUMENT_SEPARATOR'
    STRING='STRING'
    FUNCTION='FUNCTION'
    MODULE='MODULE'
    LEFT_PARENTHESIS='LEFT_PARENTHESIS'
    LEFT_BRACES='LEFT_BRACES'
    LEFT_BRACKETS='LEFT_BRACKETS'
    RIGHT_PARENTHESIS='RIGHT_PARENTHESIS'
    RIGHT_BRACES='RIGHT_BRACES'
    RIGHT_BRACKETS='RIGHT_BRACKETS'
    GREATER_THAN_EQUAL='GREATER_THAN_EQUAL'
    LESS_THAN_EQUAL='LESS_THAN_EQUAL'
    NULL='NULL'
    COMMENT='COMMENT'
    DIFFERENT='DIFFERENT'
    LESS_THAN='LESS_THAN'
    GREATER_THAN='GREATER_THAN'
    DIVISION='DIVISION'
    REMAINDER='REMAINDER'
    SUBTRACTION='SUBTRACTION'
    SUM='SUM'
    MULTIPLICATION='MULTIPLICATION'
    POWER='POWER'
    COLON='COLON'
    DOT='DOT'
    EQUAL='EQUAL'
    NOT='NOT'
    OR='OR'
    AND='AND'
    END_OF_FILE='END_OF_FILE'
    NEWLINE='NEWLINE'
    IDENTITY='IDENTITY'
    DO='DO'
    END='END'
    IN='IN'
    IF='IF'
    ELSE='ELSE'
    ATTRIBUTE='ATTRIBUTE'


class NodeType:
    STRUCT='STRUCT'
    PROGRAM='PROGRAM'
    IF_STATEMENT='IF_STATEMENT'
    BINARY_OPERATION='BINARY_OPERATION'
    BINARY_CONDITIONAL='BINARY_CONDITIONAL'
    INTEGER='INTEGER'
    FORMULA='FORMULA'
    FLOAT='FLOAT'
    STRING='STRING'
    DATETIME='DATETIME'
    BOOLEAN='BOOLEAN'
    NULL='NULL'
    UNARY_OPERATION='UNARY_OPERATION'
    UNARY_CONDITIONAL='UNARY_CONDITIONAL'
    BOOLEAN_OPERATION='BOOLEAN_OPERATION'
    BLOCK='BLOCK'
    ASSIGN='ASSIGN'
    VARIABLE='VARIABLE'
    MODULE_DEFINIITION='MODULE_DEFINIITION'
    MODULE_LITERAL='MODULE_LITERAL'
    FUNCTION_DEFINITION='FUNCTION_DEFINITION'
    FUNCTION_CALL='FUNCTION_CALL'
    LIST='LIST'
    DICT='DICT'
    SLICE='SLICE'
    ATTRIBUTE='ATTRIBUTE'


class Settings:
    def __init__(self, context=Context(), timezone='GMT', is_testing=False):
        """
        This is the settings class, this is used on the interpreter, parser and lexer.
        The idea is that with the settings we are able to translate the formula or in other words, the programming language,
        how we actually want. 

        This way, people in Brazil, in United States or Europe can adapt the formulas the way it fits them most.
        For example, in some places like Brazil float numbers are written with ',' as the decimal separator. In others like
        the United States, '.' is prefered.

        Settings is an object that needs to be passed arround inside of flow. You create a single Settings instance before running your flow script
        and then pass it around. You will see that the interpreter, parser and lexer, all of them, recieves the settings instance.

        In the interpreter you will see that all of the Flow objects like strings, Float, Structs and so on recieves the settings object. Even the default bultin library 
        recieves the settings class, that's because we need it to know what we should do.

        This is actually one of the main differences that makes Flow what it is. We bound the evaluation to a context, this way we can keep it easy to manage.

        WHY DO YOU NOT CREATE A GLOBAL SETTINGS?
        Because of the context. If this was a language running in someones computer we wouldn't need to do this but since this is a single server and 
        will probably need to handle multiple requests the Settings will change for each user. So we need to pass this instance around. That's the "easiest" way to handle this.

        WHY NOT USE CONTEXT DIRECTLY SINCE IT'S BASICALLY THE SAME?
        THe Context object is a class that holds another classes/objects. It works like the Facade Pattern for my understanding (i don't know much about them). Because of this, Context
        can change the code more often than Settings, here we have a more structured way of defining the values that will not change often. Also this can hold other stuff that
        is not context related but more general functions/methods on how the language work.

        Since this is passed around, you can add multiple handy methods here. But try to keep it as clean as possible. See that instead of context.keyword.inversion we use 
        inversion_keyword attribute only, so it's a simple flat key to check. This make it easier to retrieve stuff when needed. 

        Args:
            context (reflow_server.formula.utils.context.Context): The context class so we can translate the language in other
                                                                   languages.
        """
        self.is_testing = is_testing
        self.sigil_string = '~'
        self.attribute_character = '.'
        self.comment_character = '#'
        self.string_delimiters = ['`','"']
        self.operation_characters = ['>' ,'<', '=', '!', '/', '+', '*', '%', '-', '^', ':']
        self.valid_numbers_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.valid_braces = ['{', '}', '(', ')', '[', ']']
        self.timezone = timezone
        self.datetime_helper = DatetimeHelper()

        self.flow_context = context.flow_context
        self.reflow_automation_action_data = context.reflow.automation.action_data
        self.reflow_automation_trigger_data = context.reflow.automation.trigger_data
        self.reflow_automation_id = context.reflow.automation.id
        self.reflow_company_id = context.reflow.company_id
        self.reflow_user_id = context.reflow.user_id
        self.reflow_dynamic_form_id = context.reflow.formula.dynamic_form_id

        self.datetime_date_character = context.datetime.date_character
        self.datetime_date_format = context.datetime.date_format
        self.datetime_time_format = context.datetime.time_format
        self.positional_argument_separator = context.positional_argument_separator
        self.decimal_point_character = context.decimal_point_separator
        self.inversion_keyword = context.keyword.inversion
        self.include_keyword = context.keyword.includes
        self.disjunction_keyword = context.keyword.disjunction
        self.conjunction_keyword = context.keyword.conjunction
        self.function_keyword = context.keyword.function
        self.module_keyword = context.keyword.module
        self.null_keyword = context.keyword.null
        self.block_keywords = {
            'do': context.keyword.block.do,
            'end': context.keyword.block.end
        }
        self.if_keywords = {
            'if': context.keyword.if_block.if_keyword,
            'else': context.keyword.if_block.else_keyword
        }
        self.boolean_keywords = {
            'true': context.keyword.boolean.true,
            'false': context.keyword.boolean.false
        }
        self.library = context.library

    def time_format_to_regex(self, match_the_format=False):
        """
        This needs to live here and not in the helper because this is a helper that uses the data from the context.
        Also this caches the format of the context so we don't need to re-evaluate everytime.

        Args:
            match_the_format (bool, optional): Regex for matching the format and not the value. "What?" 
                                               Instead of a regex like \d{4} for example to match year we will generate something like
                                               (YYYY), in other words, this matches the `YYYY-MM-DD` format and not the value. Defaults to False.

        Returns:
            str: The regex to be used on the format or on the value
        """
        if match_the_format and hasattr(self, 'cached_datetime_time_format_regex'):
            return self.cached_datetime_time_format_regex

        time_format = self.datetime_time_format
        characters_that_doesnt_mean_anything = self.datetime_time_format
        for key in self.datetime_helper.valid_formats:
            time_format = time_format.replace(key, f'({key})' if match_the_format else self.datetime_helper.get_regex(key))
            characters_that_doesnt_mean_anything = characters_that_doesnt_mean_anything.replace(key, '')

        characters_that_doesnt_mean_anything = set(characters_that_doesnt_mean_anything)
        for_regex = ''.join([f"\{character}" for character in characters_that_doesnt_mean_anything])
        other_strings_regex = f"([{for_regex}])"
        time_format = re.sub(other_strings_regex, other_strings_regex + '?', time_format)
        
        if match_the_format:
            self.cached_datetime_time_format_regex = time_format
        return time_format

    def date_format_to_regex(self, match_the_format=False):
        if match_the_format and hasattr(self, 'cached_datetime_date_format_regex'):
            return self.cached_datetime_date_format_regex

        date_format = self.datetime_date_format
        for key in self.datetime_helper.valid_formats:
            date_format = date_format.replace(key, f'({key})' if match_the_format else self.datetime_helper.get_regex(key))
        
        if match_the_format:
            self.cached_datetime_date_format_regex = date_format
        return date_format

    def validate_character_for_identity_or_keywords(self, character, is_first_character=False):
        pattern = re.compile('(?!\d)([\w_])' if is_first_character else'[\w_]')
        return len(pattern.findall(character)) > 0 if isinstance(character, str) else False

    def initialize_builtin_library(self, record):
        """
        Responsible for initializing the library so users can use our builtin library in their scripts.

        Args:
            record (reflow_server.formula.utils.memory.Record): The record of the program which is responsible for holding all
                                                                of the variables.
        """
        if self.is_testing:
            from reflow_server import settings
        else:
            from django.conf import settings 

        module_names = settings.FORMULA_MODULES['default'] + settings.FORMULA_MODULES.get(self.flow_context, [])
        for formula_module_name in module_names:
            path = "%s.%s" % (settings.FORMULA_BUILTIN_MODULES_PATH, formula_module_name)
            module = __import__(path, fromlist=[formula_module_name])
            kls = getattr(module, formula_module_name)
            formula_builtin_module = kls(self)._initialize_(record)
            record.assign(formula_builtin_module.module_name, formula_builtin_module)
    