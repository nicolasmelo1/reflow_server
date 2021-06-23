from reflow_server.formula.utils.settings import TokenType, NodeType
from reflow_server.formula.utils.parser import nodes


class Parser:
    def __init__(self, lexer, settings):
        self.lexer = lexer
        self.settings = settings
        self.current_token = self.lexer.get_next_token

    def parse(self):
        node = self.program()
        return node

    def get_next_token(self, token_type):
        if token_type == self.current_token.token_type:
            self.current_token = self.lexer.get_next_token
        else:
            raise Exception('Expected token: ${tokenType}, current token: ${currentToken.tokenType}')
        
    def program(self):
        """
        program: block END_OF_FILE

        Raises:
            Exception: When the last token is not END_OF_FILE
        """
        block_node = self.block()
        program_node = nodes.Program(block_node)
        if self.current_token.token_type != TokenType.END_OF_FILE:
            raise Exception('Unexpected end of file, this means your program cannot be executed and was ended abruptly')

        return program_node

    def block(self):
        """
        block: statements_list 
        """
        instructions = self.statements_list([])
        return nodes.Block(instructions)

    def statements_list(self, instructions = []):
        """
        statement_list: (statement NEWLINE)*
        """
        node = self.statement()
        if node != None:
            instructions.append(node)
        if (TokenType.NEWLINE == self.current_token.token_type):
            self.get_next_token(TokenType.NEWLINE)
            return self.statements_list(instructions)
        else:
            return instructions

    def statement(self):
        """
        statement: compoundStatement
                 | assignment
        """
        node = self.compound_statement()
        if node:
            return node
        else:
            return self.assignment()
    
    def compound_statement(self):
        """
        compound_statement: IF if_statement 
                          | FUNCTION function_statement
        """
        if (TokenType.IF == self.current_token.token_type):
            return self.if_statement()
        elif (TokenType.FUNCTION == self.current_token.token_type):
            return self.function_statement()
    
    def assignment(self):
        """
        assignment: variable ASSIGN expression
                  | expression
        """
        node = self.expression()

        if (TokenType.ASSIGN == self.current_token.token_type):
            operation = self.current_token
            left = node
            self.get_next_token(self.current_token.token_type)
            right = self.expression()
            if (left.node_type != NodeType.VARIABLE):
                raise Exception("Cannot assign, needs to assign value to a variable")
            elif (right == None):
                raise Exception("You forgot to assign a value to a variable")
            
            return nodes.Assign(left, right, operation)
        else:
            return node
    
    def if_statement(self):
        """
        if_statement: IF expression DO block ((ELSE else_statement)? | END) 
        """
        if TokenType.IF == self.current_token.token_type:
            self.get_next_token(TokenType.IF)
            expression = self.expression()
            self.get_next_token(TokenType.DO)
            block = self.block()
            else_statement = None
            if (TokenType.ELSE == self.current_token.token_type):
                else_statement = self.else_statement()
            else:
                self.get_next_token(TokenType.END)
            return nodes.IfStatement(expression, block, else_statement)
    
    def else_statement(self):
        """
        else_statement: (ELSE DO block | ELSE IF if_statement) END
        """
        if TokenType.ELSE == self.current_token.token_type:
            self.get_next_token(TokenType.ELSE)
            if TokenType.IF == self.current_token.token_type:
                return self.if_statement()
            else:
                self.get_next_token(TokenType.DO)
                node = self.block() 
                self.get_next_token(TokenType.END)
                return node

    def function_statement(self):
        """
        function_statement: FUNCTION IDENTITY LEFT_PARENTHESIS (parameters)?* RIGHT_PARENTHESIS DO block END
        """
        if TokenType.FUNCTION == self.current_token.token_type:
            self.get_next_token(TokenType.FUNCTION)

            function_variable = self.variable()

            self.get_next_token(TokenType.IDENTITY)
            self.get_next_token(TokenType.LEFT_PARENTHESIS)

            parameters = list()
            if TokenType.IDENTITY == self.current_token.token_type:
                parameters = self.parameters([])

            self.get_next_token(TokenType.RIGHT_PARENTHESIS)
            self.get_next_token(TokenType.DO)

            function_block = self.block()

            self.get_next_token(TokenType.END)
            return nodes.FunctionDefinition(function_variable, parameters, function_block)

    def parameters(self, parameters_list=[]):
        """
        parameters: ((IDENTITY | assignment) POSITIONAL_ARGUMENT_SEPARATOR)*
        """
        if TokenType.IDENTITY == self.current_token.token_type:
            node = self.assignment()
            parameters_list.append(node)
            if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
                return self.parameters(parameters_list)
            else:
                return parameters_list
            
    def function_call_statement(self, function_name=None, function_arguments=[]):
        """
        function_call: IDENTITY LEFT_PARENTHESIS (expression POSITIONAL_ARGUMENT_SEPARATOR)?* RIGHT_PARENTHESIS
        """
        if function_name == None:
            function_name = self.current_token.value
            self.get_next_token(TokenType.IDENTITY)
            self.get_next_token(TokenType.LEFT_PARENTHESIS)
        if TokenType.RIGHT_PARENTHESIS != self.current_token.token_type:
            argument = self.expression()
            function_arguments.append(argument)
            if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
            
            return self.function_call_statement(function_name, function_arguments)
        else:
            self.get_next_token(TokenType.RIGHT_PARENTHESIS)
            return nodes.FunctionCall(function_name, function_arguments)
    
    def expression(self):
        """
        expression: disjunction
        """
        node = self.disjunction()
        return node

    def disjunction(self):
        """
        disjunction: (disjunction ((OR) | disjunction)*
                   | conjunction
        """
        node = self.conjunction()

        if TokenType.OR == self.current_token.token_type:
            operation = self.current_token
            left = node
            
            self.get_next_token(self.current_token.token_type)

            right = self.disjunction()
            if left == None or right == None:
                raise Exception("Ops, looks like you forgot to finish the 'or' expression")
            return nodes.BooleanOperation(left, right, operation)
        else:
            return node

    def conjunction(self):
        """
        conjunction : (conjunction ((AND) | conjunction)*
                    | inversion
        """
        node = self.inversion()

        if TokenType.AND == self.current_token.token_type:
            operation = self.current_token
            left = node

            self.get_next_token(self.current_token.token_type)

            right = self.conjunction()
            if left == None or right == None:
                raise Exception("Ops, looks like you forgot to finish the 'and' expression")

            return nodes.BooleanOperation(node, right, operation)
        else:
            return node

    def inversion(self):
        node = self.comparison()

        if TokenType.NOT == self.current_token.token_type:
            operation = self.current_token
            self.get_next_token(self.current_token.token_type)
            value = self.inversion()
            if value == None:
                raise Exception("You forgot to close the 'not' operator")
            return nodes.UnaryConditional(operation, value)
        else:
            return node
    
    def comparison(self):
        node = self.add()
        if self.current_token.token_type in [
            TokenType.GREATER_THAN, 
            TokenType.GREATER_THAN_EQUAL,
            TokenType.DIFFERENT,
            TokenType.LESS_THAN,
            TokenType.LESS_THAN_EQUAL,
            TokenType.EQUAL
        ]:
            operation = self.current_token
            left = node
            self.get_next_token(self.current_token.token_type)
            right = self.comparison()

            if left == None or right == None:
                raise Exception("You are comparing apples to nothing")
            return nodes.BinaryConditional(left, right, operation)
        else:
            return node
        
    def add(self):
        node = self.product()

        if self.current_token.token_type in [
            TokenType.SUM, 
            TokenType.SUBTRACTION
        ]:
            operation = self.current_token
            left = node
            self.get_next_token(self.current_token.token_type)
            right = self.add()
            return nodes.BinaryOperation(left, right, operation)
        else:
            return node

    def product(self):
        node = self.power()

        if self.current_token.token_type in [
            TokenType.DIVISION, 
            TokenType.REMAINDER, 
            TokenType.MULTIPLICATION
        ]:
            operation = self.current_token
            left = node
            self.get_next_token(self.current_token.token_type)
            right = self.product()
            return nodes.BinaryOperation(left, right, operation)
        else:
            return node

    def power(self):
        node = self.unary()

        if TokenType.POWER == self.current_token.token_type:
            operation = self.current_token
            left = node
            self.get_next_token(self.current_token.token_type)
            right = self.product()
            return nodes.BinaryOperation(left, right, operation)
        else:
            return node

    def unary(self):
        if self.current_token.token_type in [
            TokenType.SUM,
            TokenType.SUBTRACTION,
        ]:
            operation = self.current_token
            self.get_next_token(self.current_token.token_type)
            value = self.unary()
            return nodes.UnaryOperation(operation, value)
        else:
            return self.atom()
    
    def atom(self):
        token = self.current_token
        if TokenType.IDENTITY == self.current_token.token_type and self.lexer.peek_and_validate('(', 0):
            return self.function_call_statement(None, [])
        elif TokenType.BOOLEAN == self.current_token.token_type:
            node = nodes.Boolean(token)
            self.get_next_token(self.current_token.token_type)
            return node
        elif TokenType.INTEGER == self.current_token.token_type:
            node = nodes.Integer(token)
            self.get_next_token(self.current_token.token_type)
            return node
        elif TokenType.NULL == self.current_token.token_type:
            node = nodes.Null(token)
            self.get_next_token(self.current_token.token_type)
            return node
        elif TokenType.STRING == self.current_token.token_type:
            node = nodes.String(token)
            self.get_next_token(self.current_token.token_type)
            return node
        elif TokenType.FLOAT == self.current_token.token_type:
            node = nodes.Float(token)
            self.get_next_token(self.current_token.token_type)
            return node
        elif TokenType.LEFT_PARENTHESIS == self.current_token.token_type:
            node = self.expression()
            self.get_next_token(self.current_token.token_type)
            return node
        elif TokenType.IDENTITY == self.current_token.token_type:
            node = self.variable()
            self.get_next_token(self.current_token.token_type)
            return node
    
    def variable(self):
        return nodes.Variable(self.current_token)
