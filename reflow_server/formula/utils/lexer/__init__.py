from reflow_server.formula.utils.lexer.tokens import Token
from reflow_server.formula.utils.settings import TokenType


class Lexer:
    def __init__(self, expression, settings):
        self.settings = settings
        self.expression = list(expression)
        self.current_position = 0

    def advance_next_position(self, positions_to_advance=1):
        self.current_position += positions_to_advance

    def peek_next_character(self, number_of_characters_to_peek=1):
        position = self.current_position + number_of_characters_to_peek
        if position <= (len(self.expression) - 1):
            return self.expression[position]
        else:
            return None
        
    def peek_and_validate(self, character, number_of_characters_to_peek=1):
        return self.peek_next_character(number_of_characters_to_peek) == character

    def __current_token_is_space_or_tab(self):
        return self.current_position < len(self.expression) - 1 and self.expression[self.current_position] in [' ', '\t']

    def __handle_current_token(self):
        if self.current_position < len(self.expression):
            # be aware, the ordering of the conditions here are extremely important.
            # we can have numbers on variables, but if the first character is a number, it must be considered as a number
            # AND NOT a keyword. If we changed the order 1234 would be an Identity and not a Number.
            if self.expression[self.current_position] == self.settings.string_delimiter:
                return self.__handle_string()
            elif self.expression[self.current_position] in self.settings.valid_numbers_characters:
                return self.__handle_number()
            elif self.expression[self.current_position] in self.settings.valid_characters_for_identity_or_keywords:
                return self.__handle_keyword()
            elif self.expression[self.current_position] in self.settings.operation_characters:
                return self.__handle_operation()
            elif self.expression[self.current_position] in self.settings.valid_braces:
                return self.__handle_braces()
            elif self.expression[self.current_position] == self.settings.comment_character:
                return self.__handle_comment()
            elif self.expression[self.current_position] == '\n':
                self.advance_next_position()
                return Token(TokenType.NEWLINE, '\n')
            elif self.expression[self.current_position] == self.settings.positional_argument_separator:
                self.advance_next_position()
                return Token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR, self.settings.positional_argument_separator)
            else:
                raise Exception('invalid character: {}'.format(self.expression[self.current_position]))
        return Token(TokenType.END_OF_FILE, None)

    def __handle_braces(self):
        if self.expression[self.current_position] == '(':
            self.advance_next_position()
            return Token(TokenType.LEFT_PARENTHESIS, '(')
        elif self.expression[self.current_position] == ')':
            self.advance_next_position()
            return Token(TokenType.RIGHT_PARENTHESIS, ')')
        elif self.expression[self.current_position] == '[':
            self.advance_next_position()
            return Token(TokenType.LEFT_BRACKETS, '[')
        elif self.expression[self.current_position] == ']':
            self.advance_next_position()
            return Token(TokenType.RIGHT_BRACKETS, ']')
        elif self.expression[self.current_position] == '{':
            self.advance_next_position()
            return Token(TokenType.LEFT_BRACES, '{')
        elif self.expression[self.current_position] == '}':
            self.advance_next_position()
            return Token(TokenType.RIGHT_BRACES, '}')
        
    def __handle_number(self):
        number = []
        counter = 0
        while self.peek_next_character(counter) in self.settings.valid_numbers_characters or \
              self.peek_next_character(counter) == self.settings.decimal_point_character:
            if self.peek_next_character(counter) == self.settings.decimal_point_character and self.settings.decimal_point_character in number:
                raise Exception('Invalid number')
            number.append(self.expression[self.current_position + counter])
            counter += 1
        
        self.advance_next_position(counter)
        if self.settings.decimal_point_character in number:
            return Token(TokenType.FLOAT, ''.join(number))
        else:
            return Token(TokenType.INTEGER, ''.join(number))
    
    def __handle_comment(self):
        comment = []
        counter = 1
        while not self.peek_and_validate('\n', counter):
            comment.append(self.expression[self.current_position + counter])
            counter += 1
        self.advance_next_position(counter)
        return Token(TokenType.COMMENT, ''.join(comment))

    def __handle_string(self):
        string = []
        counter = 1
        while not self.peek_and_validate(self.settings.string_delimiter, counter): 
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

        while self.peek_next_character(counter) in self.settings.valid_characters_for_identity_or_keywords: 
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
            return Token(TokenType.TRUE, keyword)
        elif keyword == self.settings.boolean_keywords['false']:
            return Token(TokenType.FALSE, keyword)
        elif keyword == self.settings.null_keyword:
            return Token(TokenType.NULL, keyword)
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

    @property
    def get_next_token(self):
        while self.__current_token_is_space_or_tab():
            self.current_position += 1
        return self.__handle_current_token()
