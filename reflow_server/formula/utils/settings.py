from reflow_server.formula.utils.context import Context

class TokenType:
    ASSIGN='ASSIGN'
    INTEGER='INTEGER'
    FLOAT='FLOAT'
    BOOLEAN='BOOLEAN'
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


class NodeType:
    PROGRAM='PROGRAM'
    IF_STATEMENT='IF_STATEMENT'
    BINARY_OPERATION='BINARY_OPERATION'
    BINARY_CONDITIONAL='BINARY_CONDITIONAL'
    INTEGER='INTEGER'
    FORMULA='FORMULA'
    FLOAT='FLOAT'
    STRING='STRING'
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


class Settings:
    def __init__(self, context=Context()):
        """
        This is the settings class, this is used on the interpreter, parser and lexer.
        The idea is that with the settings we are able to translate the formula or in other words, the programming language
        how we actually want. 

        This way, people in Brazil, in United States or Europe can adapt the formulas the way it fits them most.
        For example, in some places like Brazil float numbers are written with ',' as the decimal separator. In others like
        the United States, '.' is prefered.

        Args:
            context (reflow_server.formula.utils.context.Context): The context class so we can translate the language in other
                                                                   languages.
        """
        self.comment_character = '#'
        self.string_delimiter = '"'
        self.operation_characters = ['>' ,'<', '=', '!', '/', '+', '*', '%', '-', '^', ':']
        self.valid_numbers_characters = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        self.valid_characters_for_identity_or_keywords = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '_'
        ] + self.valid_numbers_characters
        self.valid_braces = ['{', '}', '(', ')', '[', ']']
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
