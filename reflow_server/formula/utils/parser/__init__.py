from reflow_server.formula.utils.settings import TokenType, NodeType
from reflow_server.formula.utils.parser import nodes
from reflow_server.formula.utils.builtins.objects.Error import Error

class Parser:
    def __init__(self, lexer, settings):
        """
        ////////////////////////////////////////////////////////////
        // This is the Grammar of Reflow Formulas, it is based and inspired
        // on EBNF grammar: https://pt.wikipedia.org/wiki/Formalismo_de_Backus-Naur_Estendido
        // 
        // If you don't know what grammars are, read:
        // https://pt.wikipedia.org/wiki/Formalismo_de_Backus-Naur 
        //
        // Basically it is a way of representing a structure of a syntax. Every programming language
        // has one of this. This grammar helps us with the hole logic for the parsing.
        //
        // _ABOUT THE PARSER_
        // The parser uses recursion in order to transverse all of the tokens of the expression. The original article where
        // this was inspired from (Reference: https://ruslanspivak.com/lsbasi-part7/) uses while loops in order to transverse the
        // hole structure. I was also using this, but then i came in to conclusion that since it also uses recursion, using ONLY 
        // recursion would be easier to comprehend. (Note that recursion is an easy topic)
        // 
        // IF YOU DON'T UNDERSTAND AT FIRST DON'T WORRY, actually writting parsers is really difficult topic, and i don't know much of it either
        // I go most by trial and error. So there is a BIG room for improvement here.
        // 
        // Writting an interpreter i think that it's easier than a parser and makes a lot more sense.
        // Try to follow the tutorial above, and see how he writes it, and also try to see some parsers of famous languages (or at least the grammar)
        // and see if you can try to understand. Also feel free to write print statements here to understand everything that it is doing. 
        // I recommend reading from top to bottom, try to read what function he calls, what it returns. And try to understand the logic.
        //
        // If you still have a difficult time reading through it all, feel free to ask anytime, but try to at least read the tutorials 
        // i've added to the formulas so it can be a LOT easier to grasp the hole concept.
        ////////////////////////////////////////////////////////////
         
        program: block END_OF_FILE
        
        block: statements_list 
        
        compound_statement: IF if_statement 
                          | FUNCTION function_statement
                          | MODULE module_statement

        function_statement: FUNCTION (IDENTITY)? LEFT_PARENTHESIS (parameters)?* RIGHT_PARENTHESIS DO block END

        module_statement: MODULE IDENTITY (LEFT_PARENTHESIS (arguments)?* RIGHT_PARENTHESIS)? (DO module_block_statements_list END)?

        module_block_statements_list: (module_block_statement NEWLINE)* 

        module_block_statement: | FUNCTION function_statement
                                | MODULE module_statement
                                | assignment

        parameters: ((IDENTITY | assignment) POSITIONAL_ARGUMENT_SEPARATOR)*
        
        if_statement: IF expression DO block ((ELSE else_statement)? | END) 
        
        else_statement: (ELSE DO block | ELSE IF if_statement) END
        
        statements_list: (statement NEWLINE)* 
        
        statement: compound_statement
                 | assignment
        
        assignment: assignment ASSIGN assignment
                  | expression
     
        expression: disjunction
        
        disjunction: (disjunction ((OR) | disjunction)*
                   | conjunction
        
        conjunction: (conjunction ((AND) | conjunction)*
                   | inversion
        
        inversion: NOT inversion
                   | comparison
        
        comparison: comparison (( GREATER_THAN | GREATER_THAN_EQUAL | LESS_THAN | LESS_THAN_EQUAL | EQUAL | DIFFERENT | IN) comparison)* 
                  | add
         
        add: add ((PLUS | MINUS) add)*
           | product

        product: product ((MULTIPLACATION | DIVISION | REMAINDER) product)*
               | power
        
        power: power ((POWER) power)*
             | unary
        
        unary: (SUM | SUBTRACTION) unary
             | primary
         
        primary: atom
               | (slice)*
               | (attribute)*
               | (function_call)*

        attribute: primary ATTRIBUTE primary

        slice: primary LEFT_BRACKET (atom (POSITIONAL_ARGUMENT_SEPARATOR atom)*)? RIGHT_BRACKET

        function_call: primary LEFT_PARENTHESIS (expression (POSITIONAL_ARGUMENT_SEPARATOR expression)*)? RIGHT_PARENTHESIS

        atom: INTEGER 
            | FLOAT 
            | STRING
            | BOOLEAN
            | DATETIME
            | variable
            | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
            | LEFT_BRACES dict
            | LEFT_BRACKET array
        
        dict: LEFT_BRACES atom COLON statement (POSITIONAL_ARGUMENT_SEPARATOR atom COLON statement)* RIGHT_BRACES

        array: LEFT_BRACKET expression (POSITIONAL_ARGUMENT_SEPARATOR expression)* RIGHT_BRACKET
         
        variable: IDENTITY
        """
        self.lexer = lexer
        self.settings = settings
        self.current_token = self.lexer.get_next_token
    # ------------------------------------------------------------------------------------------
    def parse(self):
        node = self.program()
        return node
    # ------------------------------------------------------------------------------------------
    def get_next_token(self, token_type):
        if token_type == self.current_token.token_type:
            self.current_token = self.lexer.get_next_token
        else:
            Error(self.settings)._initialize_('SyntaxError','Expected token: {}, current token: {}'.format(token_type, self.current_token.token_type))
    # ------------------------------------------------------------------------------------------       
    def program(self):
        """
        program: block END_OF_FILE

        Raises:
            Exception: When the last token is not END_OF_FILE
        """
        block_node = self.block()
        program_node = nodes.Program(block_node)
        if self.current_token.token_type != TokenType.END_OF_FILE:
            Error(self.settings)._initialize_('SyntaxError', 'Unexpected end of file, this means your program cannot be executed and was ended abruptly')

        return program_node
    # ------------------------------------------------------------------------------------------
    def block(self):
        """
        block: statements_list 
        """
        instructions = self.statements_list([])
        return nodes.Block(instructions)
    # ------------------------------------------------------------------------------------------
    def statements_list(self, instructions=[]):
        """
        statement_list: (statement NEWLINE)*
        """
        node = self.statement()

        if node != None:
            instructions.append(node)

        if TokenType.NEWLINE == self.current_token.token_type:
            self.get_next_token(TokenType.NEWLINE)
            return self.statements_list(instructions)
        else:
            return instructions
    # ------------------------------------------------------------------------------------------
    def statement(self):
        """
        statement: compound_statement
                 | assignment
        """
        node = self.compound_statement()
    
        if node == None:
            node = self.assignment()            
        return node
    # ------------------------------------------------------------------------------------------
    def compound_statement(self):
        """
        compound_statement: IF if_statement 
                          | FUNCTION function_statement
                          | MODULE module_statement
        """
        if (TokenType.IF == self.current_token.token_type):
            return self.if_statement()
        elif TokenType.FUNCTION == self.current_token.token_type:
            return self.function_statement()
        elif TokenType.MODULE == self.current_token.token_type:
            return self.module_statement()
    # ------------------------------------------------------------------------------------------
    def assignment(self):
        """
        assignment: (variable | slice | attribute) ASSIGN (expression | FUNCTION function_statement)
                  | expression
        """
        node = self.expression()

        if self.current_token.token_type == TokenType.ASSIGN:
            left = node
            operation = self.current_token
            self.get_next_token(TokenType.ASSIGN)
            if TokenType.FUNCTION == self.current_token.token_type:
                right = self.function_statement()
            else:
                right = self.expression()
            if (left.node_type not in [NodeType.VARIABLE, NodeType.SLICE, NodeType.ATTRIBUTE]):
                Error(self.settings)._initialize_('SyntaxError', "Cannot assign, can only assign value to a variable, slice or attribute")
            elif (right == None):
                Error(self.settings)._initialize_('SyntaxError', "You forgot to assign a value to a variable")
            return nodes.Assign(left, right, operation)
        else:
            return node
    # ------------------------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------------------------
    def function_statement(self):
        """
        function_statement: FUNCTION (IDENTITY)? LEFT_PARENTHESIS (parameters)?* RIGHT_PARENTHESIS DO block END
        """
        if TokenType.FUNCTION == self.current_token.token_type:
            self.get_next_token(TokenType.FUNCTION)

            if TokenType.IDENTITY == self.current_token.token_type:
                function_variable = self.variable()
            else:
                function_variable = None
            self.get_next_token(TokenType.LEFT_PARENTHESIS)

            parameters = list()
            if TokenType.IDENTITY == self.current_token.token_type:
                parameters = self.parameters(parameters)

            self.get_next_token(TokenType.RIGHT_PARENTHESIS)
            self.get_next_token(TokenType.DO)

            function_block = self.block()

            self.get_next_token(TokenType.END)
            return nodes.FunctionDefinition(function_variable, parameters, function_block)
    # ------------------------------------------------------------------------------------------
    def module_statement(self):
        """
        module_statement: MODULE (IDENTITY)? LEFT_PARENTHESIS (arguments)?* RIGHT_PARENTHESIS DO module_block_statements_list END
        """
        if TokenType.MODULE == self.current_token.token_type:
            self.get_next_token(TokenType.MODULE)

            if TokenType.IDENTITY == self.current_token.token_type:
                module_variable = self.variable()
            else:
                module_variable = None

            parameters = None
            if TokenType.LEFT_PARENTHESIS == self.current_token.token_type:
                parameters = list()
                self.get_next_token(TokenType.LEFT_PARENTHESIS)

                if TokenType.IDENTITY == self.current_token.token_type:
                    parameters = self.parameters(parameters)

                self.get_next_token(TokenType.RIGHT_PARENTHESIS)

            module_block = list()
            if TokenType.DO == self.current_token.token_type:
                self.get_next_token(TokenType.DO)

                module_block = self.module_block_statements_list()
                self.get_next_token(TokenType.END)

            return nodes.ModuleDefinition(module_variable, parameters, module_block)
    # ------------------------------------------------------------------------------------------
    def module_block_statements_list(self, instructions=[]):
        """
        module_block_statements_list: (module_block_statement NEWLINE)* 
        """
        if TokenType.END != self.current_token.token_type:
            node = self.module_block_statement()
            if node != None:
                instructions.append(node)
            
        if TokenType.NEWLINE == self.current_token.token_type:
            self.get_next_token(TokenType.NEWLINE)
            return self.module_block_statements_list(instructions)
        else:
            return instructions
    # ------------------------------------------------------------------------------------------
    def module_block_statement(self):
        """
        module_block_statement: | FUNCTION function_statement
                                | MODULE module_statement
                                | assignment
        """
        
        while TokenType.NEWLINE == self.current_token.token_type:
            self.__ignore_newline()
        
        if TokenType.FUNCTION == self.current_token.token_type:
            node = self.function_statement()
            return nodes.ModuleLiteral(node.variable, node)
        elif TokenType.MODULE == self.current_token.token_type:
            node = self.module_statement()
            return nodes.ModuleLiteral(node.variable, node)
        else:
            node = self.assignment()
            if NodeType.ASSIGN == node.node_type:
                return nodes.ModuleLiteral(node.left, node)
            else:
                Error(self.settings)._initialize_('SyntaxError', 'must be an assignment, a new module or a function')
    # ------------------------------------------------------------------------------------------
    def parameters(self, parameters_list=[]):
        """
        parameters: ((IDENTITY | assignment) POSITIONAL_ARGUMENT_SEPARATOR)*
        """
        while TokenType.NEWLINE == self.current_token.token_type:
            self.__ignore_newline()

        if TokenType.IDENTITY == self.current_token.token_type:
            node = self.assignment()
            parameters_list.append(node)
            if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
                return self.parameters(parameters_list)
            else:
                return parameters_list
    # ------------------------------------------------------------------------------------------
    def arguments(self):
        arguments = []
        while TokenType.RIGHT_PARENTHESIS != self.current_token.token_type:
            if TokenType.FUNCTION == self.current_token.token_type:
                argument = self.function_statement()
            else:
                argument = self.expression()
            arguments.append(argument)
            if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
        return arguments
    # ------------------------------------------------------------------------------------------
    def expression(self):
        """
        expression: disjunction
        """
        node = self.disjunction()
        return node
    # ------------------------------------------------------------------------------------------
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
                Error(self.settings)._initialize_('SyntaxError', "Ops, looks like you forgot to finish the 'or' expression")
            return nodes.BooleanOperation(left, right, operation)
        else:
            return node
    # ------------------------------------------------------------------------------------------
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
                Error(self.settings)._initialize_('SyntaxError', "Ops, looks like you forgot to finish the 'and' expression")

            return nodes.BooleanOperation(node, right, operation)
        else:
            return node
    # ------------------------------------------------------------------------------------------
    def inversion(self):
        """
        inversion: (NOT) inversion
                 | comparison
        """
        node = self.comparison()

        if TokenType.NOT == self.current_token.token_type:
            operation = self.current_token
            self.get_next_token(self.current_token.token_type)
            value = self.inversion()
            if value == None:
                Error(self.settings)._initialize_('SyntaxError', "You forgot to close the 'not' operator")
            return nodes.UnaryConditional(operation, value)
        else:
            return node
    # ------------------------------------------------------------------------------------------
    def comparison(self):
        """
        comparison: comparison (( GREATER_THAN | GREATER_THAN_EQUAL | LESS_THAN | LESS_THAN_EQUAL | EQUAL | DIFFERENT | IN) comparison)* 
                  | add
        """
        node = self.add()

        if self.current_token.token_type in [
            TokenType.GREATER_THAN, 
            TokenType.GREATER_THAN_EQUAL,
            TokenType.DIFFERENT,
            TokenType.LESS_THAN,
            TokenType.LESS_THAN_EQUAL,
            TokenType.EQUAL,
            TokenType.IN
        ]:
            operation = self.current_token
            left = node
            self.get_next_token(self.current_token.token_type)
            right = self.comparison()

            if left == None or right == None:
                Error(self.settings)._initialize_('SyntaxError', "In your comparison, one of the values is wrong")
            return nodes.BinaryConditional(left, right, operation)
        else:
            return node
    # ------------------------------------------------------------------------------------------
    def add(self):
        """
        add: add ((PLUS | MINUS) add)*
           | product
        """
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
    # ------------------------------------------------------------------------------------------
    def product(self):
        """
        product: product ((MULTIPLACATION | DIVISION | REMAINDER) product)*
               | power
        """
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
    # ------------------------------------------------------------------------------------------
    def power(self):
        """
        power: power ((POWER) power)*
             | unary
        """
        node = self.unary()

        if TokenType.POWER == self.current_token.token_type:
            operation = self.current_token
            left = node
            
            self.get_next_token(TokenType.POWER)
            right = self.product()
            return nodes.BinaryOperation(left, right, operation)
        else:
            return node
    # ------------------------------------------------------------------------------------------
    def unary(self):
        """
        unary: (SUM | SUBTRACTION) unary
             | primary
        """
        if self.current_token.token_type in [
            TokenType.SUM,
            TokenType.SUBTRACTION,
        ]:
            operation = self.current_token
            self.get_next_token(self.current_token.token_type)
            value = self.unary()
            return nodes.UnaryOperation(operation, value)
        else:
            node = self.primary()
            return node
    # ------------------------------------------------------------------------------------------
    def primary(self):
        """
        primary: atom
               | struct
               | (slice)*
               | (attribute)*
               | (function_call)*

        attribute: primary ATTRIBUTE primary

        slice: primary LEFT_BRACKET (atom (POSITIONAL_ARGUMENT_SEPARATOR atom)*)? RIGHT_BRACKET

        function_call: primary LEFT_PARENTHESIS (expression (POSITIONAL_ARGUMENT_SEPARATOR expression)*)? RIGHT_PARENTHESIS
        """
        node = self.atom()

        if self.current_token.token_type in [TokenType.LEFT_PARENTHESIS, TokenType.LEFT_BRACKETS, TokenType.ATTRIBUTE, TokenType.LEFT_BRACES]:
            # this is in a while because i can have a function that returns a function like 
            # function do_something() do
            #   function another_one() do
            #       "result"
            #   end
            # end
            # 
            # do_something()() -> Will be "result"
            while self.current_token.token_type in [TokenType.LEFT_PARENTHESIS, TokenType.LEFT_BRACKETS, TokenType.ATTRIBUTE]:
                if TokenType.ATTRIBUTE == self.current_token.token_type:
                    self.get_next_token(TokenType.ATTRIBUTE)
                    right_value = self.current_token
                    node = nodes.Attribute(node, right_value)
                    self.get_next_token(TokenType.IDENTITY)

                if TokenType.LEFT_BRACKETS == self.current_token.token_type:
                    self.get_next_token(TokenType.LEFT_BRACKETS)
                    slice_value = self.expression()
                    node = nodes.Slice(node, slice_value)
                    self.get_next_token(TokenType.RIGHT_BRACKETS)

                if TokenType.LEFT_PARENTHESIS == self.current_token.token_type:
                    self.get_next_token(TokenType.LEFT_PARENTHESIS)
                    function_arguments = []
                    while TokenType.RIGHT_PARENTHESIS != self.current_token.token_type:
                        self.__ignore_newline()

                        if TokenType.FUNCTION == self.current_token.token_type:
                            argument = self.function_statement()
                        else:
                            argument = self.statement()
                        self.__ignore_newline()
                        
                        function_arguments.append(argument)
                        if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                            self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
                    self.get_next_token(TokenType.RIGHT_PARENTHESIS)
                    node = nodes.FunctionCall(node, function_arguments)

            # defines a struct
            if self.current_token.token_type == TokenType.LEFT_BRACES:
                self.get_next_token(TokenType.LEFT_BRACES)
                struct_arguments = []
                while TokenType.RIGHT_BRACES != self.current_token.token_type:
                    
                    self.__ignore_newline()

                    if TokenType.FUNCTION == self.current_token.token_type:
                        argument = self.function_statement()
                    else:
                        argument = self.statement()
                    struct_arguments.append(argument)
                    if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                        self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
                    
                    self.__ignore_newline()
                    
                self.get_next_token(TokenType.RIGHT_BRACES)
                node = nodes.Struct(node, struct_arguments)

            return node
        else:
            return node
    # ------------------------------------------------------------------------------------------
    def atom(self):
        """
        atom: INTEGER 
            | FLOAT 
            | STRING
            | BOOLEAN
            | variable
            | LEFT_PARENTHESIS expression RIGHT_PARENTHESIS
            | LEFT_BRACES dicts
            | LEFT_BRACKET array
        """
        token = self.current_token
        if TokenType.LEFT_BRACKETS == self.current_token.token_type:
            return self.array()
        elif TokenType.LEFT_BRACES == self.current_token.token_type:
            return self.dicts()
        elif TokenType.BOOLEAN == self.current_token.token_type:
            node = nodes.Boolean(token)
            self.get_next_token(TokenType.BOOLEAN)
            return node
        elif TokenType.INTEGER == self.current_token.token_type:
            node = nodes.Integer(token)
            self.get_next_token(TokenType.INTEGER)
            return node
        elif TokenType.DATETIME == self.current_token.token_type:
            node = nodes.Datetime(token)
            self.get_next_token(TokenType.DATETIME)
            return node
        elif TokenType.NULL == self.current_token.token_type:
            node = nodes.Null()
            self.get_next_token(TokenType.NULL)
            return node
        elif TokenType.STRING == self.current_token.token_type:
            node = nodes.String(token)
            self.get_next_token(TokenType.STRING)
            return node
        elif TokenType.FLOAT == self.current_token.token_type:
            node = nodes.Float(token)
            self.get_next_token(TokenType.FLOAT)
            return node
        elif TokenType.LEFT_PARENTHESIS == self.current_token.token_type:
            self.get_next_token(TokenType.LEFT_PARENTHESIS)
            node = self.statement()
            self.get_next_token(TokenType.RIGHT_PARENTHESIS)
            return node
        elif TokenType.IDENTITY == self.current_token.token_type:
            node = self.variable()
            return node
    # ------------------------------------------------------------------------------------------
    def variable(self):
        """
        variable: IDENTITY
        """
        if TokenType.IDENTITY == self.current_token.token_type:
            node = nodes.Variable(self.current_token)
            self.get_next_token(TokenType.IDENTITY)
            return node
    # ------------------------------------------------------------------------------------------
    def array(self):
        """
        array: LEFT_BRACKET (expression | function_statement) (POSITIONAL_ARGUMENT_SEPARATOR (expression | function_definition))* RIGHT_BRACKET
        """
        members = []
        if TokenType.LEFT_BRACKETS == self.current_token.token_type:
            self.get_next_token(TokenType.LEFT_BRACKETS)
            
            while TokenType.RIGHT_BRACKETS != self.current_token.token_type:
                self.__ignore_newline()

                if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                    self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
                
                self.__ignore_newline()

                if TokenType.FUNCTION == self.current_token.token_type:
                    node = self.function_statement()
                else:
                    node = self.expression()

                self.__ignore_newline()

                members.append(node)

            self.get_next_token(TokenType.RIGHT_BRACKETS)
            return nodes.List(members)
    # ------------------------------------------------------------------------------------------
    def dicts(self):
        """
        dict: LEFT_BRACES atom COLON (expression | function_statement) (POSITIONAL_ARGUMENT_SEPARATOR atom COLON (expression | function_statement))* RIGHT_BRACES
        """
        members = []

        if TokenType.LEFT_BRACES == self.current_token.token_type:
            self.get_next_token(TokenType.LEFT_BRACES)

            while TokenType.RIGHT_BRACES != self.current_token.token_type:
                self.__ignore_newline()

                key = self.atom()
                
                self.__ignore_newline()

                self.get_next_token(TokenType.COLON)

                self.__ignore_newline()

                if TokenType.FUNCTION == self.current_token.token_type:
                    value = self.function_statement()
                else:
                    value = self.expression()

                self.__ignore_newline()
                members.append([key, value])

                if TokenType.POSITIONAL_ARGUMENT_SEPARATOR == self.current_token.token_type:
                    self.get_next_token(TokenType.POSITIONAL_ARGUMENT_SEPARATOR)
                self.__ignore_newline()

            self.get_next_token(TokenType.RIGHT_BRACES)

            return nodes.Dict(members)
    # ------------------------------------------------------------------------------------------
    def __ignore_newline(self):
        if TokenType.NEWLINE == self.current_token.token_type:
            self.get_next_token(TokenType.NEWLINE)