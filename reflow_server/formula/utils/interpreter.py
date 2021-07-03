from reflow_server.formula.utils.settings import NodeType, TokenType
from reflow_server.formula.utils.memory import Memory, Record
from reflow_server.formula.utils import builtins
from reflow_server.formula.utils import helpers

import types


class Interpreter:
    def __init__(self, settings):
        self.settings = settings
        self.global_memory = Memory()

    def evaluate(self, node, evaluate_function_call=False):
        """
        Main function of the interpreter, if you check the return of the `interpreter` function it is the result of this
        
        This works recusively, if you see clearly, whenever we handle a node we call this function is called again. By making this way 
        this we can interpret the hole Abstract Syntax Tree of the program. Also by returning EVERY handle call, we guarantee that the
        program will return something to the user. This is why this is a FUNCTIONAL Language and not a Object Oriented Programming language.
        
        One thing you must understand now is `evaluate_function_call`. We need to do this because `.handle_function_call()` can return
        a value or a function. And you might ask yourself why.
        
        First read here: https://en.wikipedia.org/wiki/Tail_call

        Since this is a FUNCTIONAL language we will generaly use recursion to achieve a loop. So what do we do?
        Let's see two examples:

        EXAMPLE 1:
            function fibonacci(n) do
                if n <= 1 do
                    n
                else do
                    fibonacci(n - 1) + fibonacci(n - 2)
                end
            end

            fibonacci(5)

        EXAMPLE 2:
            function fibonacci(n; a=0; b=1) do
                if n == 0 do
                    a
                else if n == 1 do
                    b
                else do
                    fibonacci(n - 1; b; a + b)
                end
            end

            fibonacci(5)

        If you read the wikipedia article you have understood that on EXAMPLE 1 we DON'T HAVE a Tail Recursion, and on the second one
        we have Tail Recursion.
        So how does it work?

        The call stack on each iteration of the first function will look something like this:
        ----------------------------------------------------------------
        |     Iter 1   ||     Iter 2   ||     Iter 3   ||     Iter 4   |   
        ----------------------------------------------------------------
        | fibonacci(5) || fibonacci(4) || fibonacci(3) || fibonacci(2) |
        ----------------| fibonacci(3) || fibonacci(2) || fibonacci(1) |
                        |--------------|| fibonacci(2) || fibonacci(1) |
                                        | fibonacci(1) || fibonacci(0) |
                                        ----------------| fibonacci(1) |
                                                        | fibonacci(0) |
                                                        | fibonacci(0) |
                                                        | fibonacci(-1)|
                                                        ----------------
        
        in other words: each call to fibonacci function in the first example adds two more calls to the callstack. It doesn't work
        EXACTLY like this but you get it, the difficulty is added by a factor of 2.
        The call stack on this example, on the Iteration 4, we have 3 functions with fibonacci(1) and fibonacci(0), so you might expect
        on the next iteration that those function calls leave the call stack.
        Also something about callstack: remember that fibonacci(5) is still waiting for the result. so this function still is in the call
        stack so in general the call stack would look something like this (we add to the call stack on each iteration)
        ----------------------------------------------------------------
        |     Iter 1   ||     Iter 2   ||     Iter 3   ||     Iter 4   |   
        ----------------------------------------------------------------
        | fibonacci(5) || fibonacci(5) || fibonacci(5) || fibonacci(5) |
        ----------------| fibonacci(4) || fibonacci(4) || fibonacci(4) |
                        | fibonacci(3) || fibonacci(3) || fibonacci(3) |
                        ----------------| fibonacci(2) || fibonacci(2) |
                                        | fibonacci(2) || fibonacci(2) |
                                        | fibonacci(2) || fibonacci(2) |
                                        | fibonacci(1) || fibonacci(1) |
                                        ----------------| fibonacci(1) |
                                                        | fibonacci(1) |
                                                        | fibonacci(0) |
                                                        | fibonacci(1) |
                                                        | fibonacci(0) |
                                                        | fibonacci(0) |
                                                        | fibonacci(-1)|
                                                        ----------------

        so fibonacci(5) on the first example is 2^5 - So we need 32 loops to give the result. It is rather quickly. But when we put 
        fibonacci(30) our code will make 2^30 = 1.073.741.824 loops to retrieve the result, this actually doesn't fill the call stack but takes
        too long to run.

        On the first example we can't make any optimizations but let's take a look on the callstack of the second example if we 
        haven't made any optimizations:
        ----------------------------------------------------------------------------------------
        |       Iter 1       ||       Iter 2       ||       Iter 3       ||       Iter 4       |
        ----------------------------------------------------------------------------------------
        | fibonacci(5; 0, 1) || fibonacci(5; 0, 1) || fibonacci(5; 0, 1) || fibonacci(5; 0, 1) |
        |--------------------|| fibonacci(4; 1, 1) || fibonacci(4; 1, 1) || fibonacci(4; 1, 1) |
                              |--------------------|| fibonacci(3; 1, 2) || fibonacci(3; 1, 2) |
                                                    |--------------------|| fibonacci(2; 2, 3) |
                                                                          |--------------------|

        Did you notice something different? For every iteration we add a new function to the call stack, which is better than the previous problem
        but this is not good, can you understand why?

        If you look closely at the CallStack class you will notice that we have a limit on how many functions we can call, which at the time of the 
        writing is 500.

        In other words, this will fill the callstack, and not only the callstack of our interpreter and virtual memory but the call stack of the 
        programming language we are using for the interpreter (in this case, Python), so how do we solve it? With a tail call optimization (TCO).

        So how does it work? When we are calling the fibonacci function we have access on what is on the peek of the callstack, we can know
        if we are in a recursion or not. So, if we are in a recursion, and the result of the hole block of code is a function (a function in the interpreters
        language, on this case, python) what we do is, we add the next function call to the same callstack of our current function.

        Our callstack would look something like

        ----------------------------------------------------------------------------------------
        |       Iter 1       ||       Iter 2       ||       Iter 3       ||       Iter 4       |
        ----------------------------------------------------------------------------------------
        | fibonacci(5; 0, 1) || fibonacci(4; 1, 1) || fibonacci(3; 1, 2) || fibonacci(2; 2, 3) |
        ----------------------------------------------------------------------------------------

        We are updating the first call stack with the next one and so on. We do this by putting the code in a while, and while the return of the evaluation
        of the block is a function (in our interpreter's programming language) we keep iterating until we get the last value.

        Args:
            node (reflow_server.formula.utils.parser.nodes.*): You might want to check nodes.py file in the parser folder for what are all
                                                               of the possible nodes.
            evaluate_function_call (bool, optional): If true we evaluate the function recieved by the '.handle_function_call()', if False
            we will not evaluate the result unless it's needed. Defaults to False.

        Returns:
            reflow_server.formula.utils.builtins.*: Generally returns an builtin object.
        """
        if node.node_type == NodeType.FUNCTION_CALL:
            function_evaluated_value = self.handle_function_call(node)
            if evaluate_function_call and isinstance(function_evaluated_value, types.FunctionType):
                return function_evaluated_value(False)
            else:
                return function_evaluated_value
        elif node.node_type == NodeType.FUNCTION_DEFINITION:
            return self.handle_function_definition(node)
        elif node.node_type == NodeType.IF_STATEMENT:
            return self.handle_if_statement(node)
        elif node.node_type == NodeType.PROGRAM:
            return self.handle_program(node)
        elif node.node_type == NodeType.VARIABLE:
            return self.handle_variable(node)
        elif node.node_type == NodeType.ASSIGN:
            return self.handle_assign(node)
        elif node.node_type == NodeType.BLOCK:
            return self.handle_block(node)
        elif node.node_type == NodeType.UNARY_OPERATION:
            return self.handle_unary_operation(node)
        elif node.node_type == NodeType.UNARY_CONDITIONAL:
            return self.handle_unary_conditional(node)
        elif node.node_type == NodeType.BINARY_CONDITIONAL:
            return self.handle_binary_conditional(node)
        elif node.node_type == NodeType.BINARY_OPERATION:
            return self.handle_binary_operation(node)
        elif node.node_type == NodeType.BOOLEAN_OPERATION:
            return self.handle_boolean_operation(node)
        elif node.node_type == NodeType.SLICE:
            return self.handle_slice(node)
        elif node.node_type == NodeType.NULL:
            return self.handle_null(node)
        elif node.node_type == NodeType.STRING:
            return self.handle_string(node)
        elif node.node_type == NodeType.FLOAT:
            return self.handle_float(node)
        elif node.node_type == NodeType.LIST:
            return self.handle_list(node)
        elif node.node_type == NodeType.INTEGER:
            return self.handle_integer(node)
        elif node.node_type == NodeType.BOOLEAN:
            return self.handle_boolean(node)
        else:
            return node
    
    def handle_program(self, node):
        record = Record('MAIN', 'PROGRAM')
        self.global_memory.stack.push(record)
        return self.evaluate(node.block)

    def handle_block(self, node):
        none = builtins.objects.Null(self.settings)
        last_value = none._initialize_()
        for instrunction in  node.instructions:
            last_value = self.evaluate(instrunction)
        return last_value

    def handle_function_definition(self, node):
        is_anonymous_function = node.variable == None
    
        function = builtins.objects.Function(self.settings)
        record = self.global_memory.stack.peek()
        function_value = function._initialize_(node, record, node.parameters)
        if not is_anonymous_function:
            function_name = node.variable.value.value
            record.assign(function_name, function_value)

        return function_value

    def handle_function_call(self, node):
        function_name = node.name
        record = self.global_memory.stack.peek()
        function_object = record.get(function_name)

        def create_function_record():
            function_record = Record(function_name,'FUNCTION')

            # Define the scope of the function in the new function call stack
            for key, value in function_object.scope.members.items():
                function_record.assign(key, value)

            # Gets the positional parameters and also the values parameters
            for index in range(len(function_object.parameters)):
                parameter_name = None
                parameter_value = None
                if index < len(node.parameters):
                    if function_object.parameters[index].node_type == NodeType.ASSIGN:
                        parameter_name = function_object.parameters[index].left.value.value 
                    else:
                        parameter_name = function_object.parameters[index].value.value 
                    parameter_value = self.evaluate(node.parameters[index])
                elif function_object.parameters[index].node_type == NodeType.ASSIGN:
                    parameter_name = function_object.parameters[index].left.value.value 
                    parameter_value = self.evaluate(function_object.parameters[index].right)
                else:
                    raise Exception('missing parameter of function "{function_name}"'.format(function_name=function_name))
                function_record.assign(parameter_name, parameter_value)
            return function_record
        
        def to_evaluate_function(push_to_current=False):
            record = create_function_record()
            if push_to_current:
                self.global_memory.stack.push_to_current(record)
            else:
                self.global_memory.stack.push(record)

            result = self.evaluate(function_object.ast_function.block)
            
            if push_to_current == False:
                self.global_memory.stack.pop()  
            return result

        # If this condition is set this means we are inside a recursion (we are in a function named fibonacci, and calling it again)
        is_in_recursion = function_name == record.name
        
        if is_in_recursion:
            return to_evaluate_function
        else:
            record = create_function_record()
            self.global_memory.stack.push(record)

            result = self.evaluate(function_object.ast_function.block)
            while isinstance(result, types.FunctionType):
                result = result(True)
        
            self.global_memory.stack.pop()
            return result

    def handle_if_statement(self, node):
        expression_value = self.evaluate(node.expression, True)
        if expression_value._boolean_()._representation_():
            return self.evaluate(node.block)
        elif node.else_statement:
            return self.evaluate(node.else_statement)
    
    def handle_assign(self, node):
        variable_value = self.evaluate(node.right, True)

        # if we assign to a normal variable
        if node.left.node_type == NodeType.VARIABLE:
            variable_name = node.left.value.value
        
            record = self.global_memory.stack.peek()
            record.assign(variable_name, variable_value)
            return variable_value
        # if we assign to a item in an array
        elif node.left.node_type == NodeType.SLICE:
            # variavel[1] -> left_of_slice is the value relative to 'variavel'
            left_of_slice = node.left 
            slices_stack = []
            while left_of_slice.node_type == NodeType.SLICE:
                slices_stack.append(self.evaluate(left_of_slice.slice))
                left_of_slice = left_of_slice.left
            if left_of_slice.node_type == NodeType.VARIABLE:
                variable_name = left_of_slice.value.value
                record = self.global_memory.stack.peek()
                root_list = record.get(variable_name)
            else:
                # root_list is the actual root of the value, for example: array[0][1] the root is 'array' variable even though we have another array inside of the array
                # so for example in an array like [1, [2, [3]]] the root_list is [1, [2, [3]]] as you might expect
                # if the value on the left is not a variable. Exemple: [1, 2, 3][1] = "Teste" should be acceptable
                root_list = self.evaluate(left_of_slice)
            
            next_list = None

            while len(slices_stack) > 0:
                list_to_change = root_list if next_list == None else next_list
                index_or_key = slices_stack.pop()
                next_list = list_to_change._getitem_(index_or_key._representation_())
        
            list_to_change._setitem_(index_or_key._representation_(), variable_value)
            return root_list

    def handle_variable(self, node):
        variable_name = node.value.value
        record = self.global_memory.stack.peek()
        return record.get(variable_name)

    def handle_binary_operation(self, node):
        value_left = self.evaluate(node.left, True)
        value_right = self.evaluate(node.right, True)
        if node.operation.token_type == TokenType.MULTIPLICATION:
            return value_left._multiply_(value_right)
        elif node.operation.token_type == TokenType.DIVISION:
            return value_left._divide_(value_right)
        elif node.operation.token_type == TokenType.SUBTRACTION:
            return value_left._subtract_(value_right)
        elif node.operation.token_type == TokenType.SUM:
            return value_left._add_(value_right)
        elif node.operation.token_type == TokenType.POWER:
            return value_left._power_(value_right)
        elif node.operation.token_type == TokenType.REMAINDER:
            return value_left._remainder_(value_right)

    def handle_boolean_operation(self, node):
        value_left = self.evaluate(node.left, True)
        value_right = self.evaluate(node.right, True)

        if node.operation.token_type == TokenType.CONJUNCTION:
            return value_left._and_(value_right)
        elif node.operation.token_type == TokenType.DISJUNCTION:
            return value_left._or_(value_right)
        
    def handle_binary_conditional(self, node):
        if node.operation.token_type in [
            TokenType.EQUAL, 
            TokenType.DIFFERENT, 
            TokenType.LESS_THAN,
            TokenType.GREATER_THAN,
            TokenType.LESS_THAN_EQUAL,
            TokenType.GREATER_THAN_EQUAL,
            TokenType.IN
        ]:
            value_left = self.evaluate(node.left, True)
            value_right = self.evaluate(node.right, True)

            if node.operation.token_type == TokenType.EQUAL:
                return value_left._equals_(value_right)
            elif node.operation.token_type == TokenType.DIFFERENT:
                return value_left._difference_(value_right)
            elif node.operation.token_type == TokenType.LESS_THAN:
                return value_left._lessthan_(value_right)
            elif node.operation.token_type == TokenType.GREATER_THAN:
                return value_left._greaterthan_(value_right)
            elif node.operation.token_type == TokenType.LESS_THAN_EQUAL:
                return value_left._lessthanequal_(value_right)
            elif node.operation.token_type == TokenType.GREATER_THAN_EQUAL:
                return value_left._greaterthanequal_(value_right)
            elif node.operation.token_type == TokenType.IN:
                # this is the opposite way, because its 10 in [1, 2, 3, 4, 10]
                # so left is the value and right is the iterable
                return value_right._in_(value_left)

    def handle_slice(self, node):
        slice_value = self.evaluate(node.slice)
        value_left = self.evaluate(node.left)
        return value_left._getitem_(slice_value._representation_())

    def handle_unary_conditional(self, node):
        if node.operation.token_type == TokenType.INVERSION:
            value = self.evaluate(node.value, True)
            return value._boolean_()._not_()

    def handle_unary_operation(self, node):
        value = self.evaluate(node.value, True)
        if node.operation.token_type == TokenType.SUM:
            return value._unaryplus_()
        elif node.operation.token_type == TokenType.SUBTRACTION:
            return value._unaryminus_()
    
    def handle_null(self, node):
        null = builtins.objects.Null(self.settings)
        return null._initialize_()

    def handle_string(self, node):
        if helpers.is_string(node.value.value):
            string = builtins.objects.String(self.settings)
            return string._initialize_(node.value.value)
        else:
            raise Exception('Cannot interpret string')

    def handle_integer(self, node):
        if helpers.is_integer(node.value.value):
            integer = builtins.objects.Integer(self.settings)
            return integer._initialize_(node.value.value)
        else:
            raise Exception('Cannot interpret integer')

    def handle_list(self, node):
        list_value = builtins.objects.List(self.settings)
        members = []
        for member in node.members:
            members.append(self.evaluate(member))
        return list_value._initialize_(members)

    def handle_float(self, node):
        value = node.value.value.replace(self.settings.decimal_point_character, '.')
        if helpers.is_float(value):
            float_value = builtins.objects.Float(self.settings)
            return float_value._initialize_(node.value.value)
        else:
            raise Exception('Cannot interpret float')

    def handle_boolean(self, node):
        if helpers.is_boolean(node.value.value):
            boolean = builtins.objects.Boolean(self.settings)
            return boolean._initialize_(node.value.value)
        else:
            raise Exception('Cannot interpret boolean')
