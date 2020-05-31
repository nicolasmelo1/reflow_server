from reflow_server.formula.utils.settings import Structure
from reflow_server.formula.exceptions import FormulaException
from reflow_server.formula.utils.tokens import Token, TokenContainer

import re

class Lexer(Structure):
    def __init__(self, expression, *args, **kwargs):
        """
        The lexer is responsible to convert a normal string to a string
        that can be interpreted by the parser. All of the strings are converted to tokens.
        Tokens are always unique. Everything is converted to tokens, excepted formulas.

        Arguments:
            expression {str} -- recieves a complete formula as a string.
        """
        super(Lexer, self).__init__(*args, **kwargs)

        self.__expression = '({})'.format(expression)
        self.token_container = TokenContainer()
        for to_tokenize in self.to_tokenize:
            matches = re.findall(to_tokenize[1], self.__expression)
            self.__tokenize(matches, to_tokenize[0], *args, **kwargs)
        self.__format_and_validate()

    @property
    def expression(self):
        """
        Returns the lexed expression, the lexed expression is tokenized values ignoring formulas, 
        and special characters as (, ) and ;
        """
        
        return self.__expression


    def __tokenize(self, matches, token_type, *args, **kwargs):
        """
        Creates a Token object based on regex expressions, each token holds the type on which type the token is,
        and the value. The tokens are saved in a variable called tokenized, it is a dict that holds all the tokens as keys
        And Token objects as value. The keys are then replaced in the expression.

        Arguments:
            matches {str - regular expression} -- List of regular expression matches from the regex
            token_type {str} -- Check types in Structure inside settings.py
        """
        for match in matches:
            key = self.token_container.add_token(match, token_type, is_first_tokenization=True, *args, **kwargs)
            self.__expression = self.__expression.replace(match, ' {} '.format(key), 1)

    def __format_and_validate(self):
        """
        Runs format and validate functions
        """

        return self.__format()

    def __format(self):
        """
        Removes all the extra spaces from the formula and adds exactly one space per item, do if the formula is as
        'SUM     ( 1; 2; 3)' we first tokenize the numbers in the __tokenize() function so we end up with 
        'SUM     ( token; token; token)' and then in this function we format and end up with
        'SUM ( token ; token ; token )' with exactly one space per item.
        """

        for character in self.valid_characters:
            self.__expression = self.__expression.replace(character, ' {} '.format(character))
        
        return self.__validate()
    
    def __validate(self):
        """
        Validates if the formula is valid, only formulas, valid characters or and tokens are valid, if it is not any of 
        them the formula is invalid. We also check for the number of parenthesis so a formula like
        `SUM (1;2;3))` will fail because of the extra parenthesis.
        """

        validate_parenthesis = [0, 0]
        for token in self.__expression:
            if token != '':
                if token in self.token_container.tokens:
                    pass
                elif self.is_formula(token.upper()): 
                    pass
                elif token in self.valid_characters:
                    if token == '(':
                        validate_parenthesis[0] += 1
                    elif token == ')':
                        validate_parenthesis[1] += 1
                else:
                    raise FormulaException('Formula not valid')
        if validate_parenthesis[0] != validate_parenthesis[1]:
            raise FormulaException('Formula not valid')
        