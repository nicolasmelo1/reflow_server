from reflow_server.formula.utils.lexer.tokens import Token
from reflow_server.formula.utils.settings import TokenType
from reflow_server.formula.utils.builtins.objects.Error import Error

import re


class Lexer:
    """
    The lexer is responsible for reading the code and transform everything into tokens.

    WHAT?

    Yep, you've probably already read the tutorials that i've added in the documentation of the formulas
    but in case you don't already know. The lexer runs in a similar manner to the parser. The parser runs until
    it finds the END_OF_FILE token. The lexer generate this token if no other token is generated.

    The idea is simple, let's suppose the following script:
    100+20

    okay so let's divide this into a list so we can pass through each character

    >>> expression = ['1', '0', '0', '+', '2', '0']
    expression[0] will be 1. the character '1' is what? a number correct? The number is just '1' or '100'? '100' correct?
    So we do not stop there, let's evaluate the next character, we've got '0'. and the next one '0'. And they are both numbers. 
    Let's go for the next one, just in case. Uoh we got '+', is it a number? No, what we've got? '1', '0' and '0' so
    the number probably is '100' so we create a new Token with the value '100'.

    Okay, but the next token is '+', let's evaluate that. It's an operation right? but operations can be ">=" or '==', in other words
    they can be two characters long. So let's evaluate the next one just to see. It's '2'. Okay, not a valid character for an operation
    so this operation is '+' so the Token will hold the value '+'

    And last but not least we evaluate '20' to a token the same way as we did for 100 up there. Then we created the last token.
    But THIS IS NOT THE LAST TOKEN. The last token WILL ALWAYS BE 'END_OF_FILE', so after we generated the Token(NUMBER,20) we 
    create the TOKEN(END_OF_FILE, None) to indicate that the program has finished evaluating.

    And that's it.

    Args:
        expression (str): The actual formula to evaluate
        settings (reflow_server.formula.utils.settings.Setting): The settings so we can translate the formula.
    """
    def __init__(self, expression, settings):
        self.settings = settings
        self.expression = list(expression)
        self.current_position = 0


    def advance_next_position(self, positions_to_advance=1):
        self.current_position += positions_to_advance

    def peek_next_token(self):
        current_position = self.current_position
        next_token = self.get_next_token
        self.current_position = current_position
        return next_token

    def peek_next_character(self, number_of_characters_to_peek=1):
        position = self.current_position + number_of_characters_to_peek
        if position <= (len(self.expression) - 1):
            return self.expression[position]
        else:
            return None
        
    def peek_and_validate(self, character, number_of_characters_to_peek=1):
        """
        If you peek from the Parser, use number_of_characters_to_peek as 0
        """
        return self.peek_next_character(number_of_characters_to_peek) == character

    def __validate_closure_of_braces(self, brace_to_close, closing_brace):
        count = 0
        while self.current_position + count < len(self.expression):
            next_character = self.peek_and_validate(closing_brace, count)
            if next_character:
                return next_character
            else:
                count += 1
        Error(self.settings)._initialize_('SyntaxError', "Need to close '{}'".format(brace_to_close))

    def __current_token_is_space_or_tab(self):
        return self.current_position < len(self.expression) - 1 and self.expression[self.current_position] in [' ', '\t']

    def __ignore_comments(self):
        if self.current_position < len(self.expression) - 1 and self.expression[self.current_position] == self.settings.comment_character:
            while self.expression[self.current_position] != '\n':
                self.current_position += 1

    def __handle_current_token(self):
        if self.current_position < len(self.expression):
            # be aware, the ordering of the conditions here are extremely important.
            # we can have numbers on variables, but if the first character is a number, it must be considered as a number
            # AND NOT a keyword. If we changed the order 1234 would be an Identity and not a Number.
            if self.expression[self.current_position] in self.settings.string_delimiters:
                return self.__handle_string()
            elif self.expression[self.current_position] in self.settings.valid_numbers_characters:
                return self.__handle_number()
            elif self.expression[self.current_position] in self.settings.sigil_string and self.peek_and_validate(self.settings.datetime_date_character) and self.peek_and_validate('[', 2):
                return self.__handle_datetime()
            elif self.settings.validate_character_for_identity_or_keywords(self.expression[self.current_position]):
                return self.__handle_keyword()
            elif self.expression[self.current_position] in self.settings.operation_characters:
                return self.__handle_operation()
            elif self.expression[self.current_position] in self.settings.valid_braces:
                return self.__handle_braces()
            elif self.expression[self.current_position] == self.settings.attribute_character:
                self.advance_next_position()
                return Token(TokenType.ATTRIBUTE, self.settings.attribute_character)
            elif self.expression[self.current_position] == '\n':
                self.advance_next_position()
                return Token(TokenType.NEWLINE, '\n')
            elif self.expression[self.current_position] == self.settings.positional_argument_separator:
                self.advance_next_position()
                return Token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR, self.settings.positional_argument_separator)
            else:
                Error(self.settings)._initialize_('SyntaxError', 'invalid character: {}'.format(self.expression[self.current_position]))
        return Token(TokenType.END_OF_FILE, None)
    
    def __handle_braces(self):
        if self.expression[self.current_position] == '(':
            self.advance_next_position()
            self.__validate_closure_of_braces('(', ')')
            return Token(TokenType.LEFT_PARENTHESIS, '(')
        elif self.expression[self.current_position] == ')':
            self.advance_next_position()
            return Token(TokenType.RIGHT_PARENTHESIS, ')')
        elif self.expression[self.current_position] == '[':
            self.advance_next_position()
            self.__validate_closure_of_braces('[', ']')
            return Token(TokenType.LEFT_BRACKETS, '[')
        elif self.expression[self.current_position] == ']':
            self.advance_next_position()
            return Token(TokenType.RIGHT_BRACKETS, ']')
        elif self.expression[self.current_position] == '{':
            self.advance_next_position()
            self.__validate_closure_of_braces('{', '}')
            return Token(TokenType.LEFT_BRACES, '{')
        elif self.expression[self.current_position] == '}':
            self.advance_next_position()
            return Token(TokenType.RIGHT_BRACES, '}')
    
    def __handle_datetime(self):
        counter = 3
        datetime = [] 
        self.__validate_closure_of_braces('[', ']')
        while self.peek_next_character(counter) != ']':
            datetime.append(self.expression[self.current_position + counter])
            counter += 1
        self.advance_next_position(counter + 1)
        return Token(TokenType.DATETIME, ''.join(datetime))

    def __handle_number(self):
        number = []
        counter = 0
        while self.peek_next_character(counter) in self.settings.valid_numbers_characters or \
              self.peek_next_character(counter) == self.settings.decimal_point_character:
            if self.peek_next_character(counter) == self.settings.decimal_point_character and self.settings.decimal_point_character in number:
                Error(self.settings)._initialize_('SyntaxError', 'Invalid number: {}'.format(''.join(number)))
            number.append(self.expression[self.current_position + counter])
            counter += 1
        
        self.advance_next_position(counter)
        if self.settings.decimal_point_character in number:
            return Token(TokenType.FLOAT, ''.join(number))
        else:
            return Token(TokenType.INTEGER, ''.join(number))

    def __handle_string(self):
        string = []
        counter = 1
        while self.peek_next_character(counter) not in self.settings.string_delimiters: 
            string.append(self.expression[self.current_position + counter])
            counter += 1
        self.advance_next_position(counter+1)
        return Token(TokenType.STRING, ''.join(string))
    
    def __handle_keyword(self):
        """
        This handles all of the keywords of the programming language
        and also the identities. The valid chacters for identity or 
        keywords can be found in settings.

        Returns:
            reflow_server.formula.utils.lexer.tokens.Token: Returns a keyword or identitys token
        """
        keyword = []
        counter = 0

        while self.settings.validate_character_for_identity_or_keywords(self.peek_next_character(counter)): 
            keyword.append(self.expression[self.current_position+counter])
            counter += 1

        self.advance_next_position(counter)
        keyword = ''.join(keyword)

        if keyword == self.settings.block_keywords['do']:
            return Token(TokenType.DO, keyword)
        elif keyword == self.settings.block_keywords['end']:
            return Token(TokenType.END, keyword)
        elif keyword == self.settings.if_keywords['if']:
            return Token(TokenType.IF, keyword)
        elif keyword == self.settings.if_keywords['else']:
            return Token(TokenType.ELSE, keyword)
        elif keyword == self.settings.boolean_keywords['true']:
            return Token(TokenType.BOOLEAN, keyword)
        elif keyword == self.settings.boolean_keywords['false']:
            return Token(TokenType.BOOLEAN, keyword)
        elif keyword == self.settings.null_keyword:
            return Token(TokenType.NULL, keyword)
        elif keyword == self.settings.module_keyword:
            return Token(TokenType.MODULE, keyword)
        elif keyword == self.settings.function_keyword:
            return Token(TokenType.FUNCTION, keyword)
        elif keyword == self.settings.conjunction_keyword:
            return Token(TokenType.AND, keyword)
        elif keyword == self.settings.disjunction_keyword:
            return Token(TokenType.OR, keyword)
        elif keyword == self.settings.inversion_keyword:
            return Token(TokenType.NOT, keyword)
        elif keyword == self.settings.include_keyword:
            return Token(TokenType.IN, keyword)
        else:
            return Token(TokenType.IDENTITY, keyword)
    # ------------------------------------------------------------------------------------------
    def __handle_operation(self):
        """
        This handles only operations in the programming languages. 
        From assign, to boolean operations like equals, different and so on,
        and last but not least math operations.

        Returns:
            reflow_server.formula.utils.lexer.tokens.Token: Returns a operation token
        """
        current_character = self.expression[self.current_position]
        # be aware, the ordering of the conditions here are extremely important.
        # first we get the conditions that match most characters, than the ones with least number of characters
        # if we had '===' we would add this condition at the top of all the other conditions.
        if current_character == '=' and self.peek_and_validate('='):
            self.advance_next_position(2)
            return Token(TokenType.EQUAL, '==')
        elif current_character == '!' and self.peek_and_validate('='):
            self.advance_next_position(2)
            return Token(TokenType.DIFFERENT, '!=')
        elif current_character == '<' and self.peek_and_validate('='):
            self.advance_next_position(2)
            return Token(TokenType.LESS_THAN_EQUAL, '<=')
        elif current_character == '>' and self.peek_and_validate('='):
            self.advance_next_position(2)
            return Token(TokenType.GREATER_THAN_EQUAL, '>=')
        elif current_character == '=':
            self.advance_next_position()
            return Token(TokenType.ASSIGN, current_character)
        elif current_character == '+':
            self.advance_next_position()
            return Token(TokenType.SUM, current_character)
        elif current_character == '-':
            self.advance_next_position()
            return Token(TokenType.SUBTRACTION, current_character)
        elif current_character == '*':
            self.advance_next_position()
            return Token(TokenType.MULTIPLICATION, current_character)
        elif current_character == '/':
            self.advance_next_position()
            return Token(TokenType.DIVISION, current_character)
        elif current_character == '^':
            self.advance_next_position()
            return Token(TokenType.POWER, current_character)
        elif current_character == '%':
            self.advance_next_position()
            return Token(TokenType.REMAINDER, current_character)
        elif current_character == '<':
            self.advance_next_position()
            return Token(TokenType.LESS_THAN, current_character)
        elif current_character == '>':
            self.advance_next_position()
            return Token(TokenType.GREATER_THAN, current_character)
        elif current_character == ':':
            self.advance_next_position()
            return Token(TokenType.COLON, current_character)
    # ------------------------------------------------------------------------------------------
    @property
    def get_next_token(self):
        while self.__current_token_is_space_or_tab():
            self.current_position += 1
        self.__ignore_comments()
        return self.__handle_current_token()
