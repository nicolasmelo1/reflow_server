from reflow_server.formula.utils.settings import NodeType, TokenType
from reflow_server.formula.utils.memory import Memory, Record
from reflow_server.formula.utils import builtins
from reflow_server.formula.utils import helpers

import types


class Interpreter:
    def __init__(self, settings):
        self.settings = settings
        self.global_memory = Memory(self.settings)
    # ------------------------------------------------------------------------------------------
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
            # if we recieve a python function than push to current. Othewise returns the actual value of the function
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
        elif node.node_type == NodeType.MODULE_DEFINIITION:
            return self.handle_module_definition(node)
        elif node.node_type == NodeType.STRUCT:
            return self.handle_struct(node)
        elif node.node_type == NodeType.ATTRIBUTE:
            return self.handle_attribute(node)
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
        elif node.node_type == NodeType.DATETIME:
            return self.handle_datetime(node)
        elif node.node_type == NodeType.FLOAT:
            return self.handle_float(node)
        elif node.node_type == NodeType.LIST:
            return self.handle_list(node)
        elif node.node_type == NodeType.DICT:
            return self.handle_dict(node)
        elif node.node_type == NodeType.INTEGER:
            return self.handle_integer(node)
        elif node.node_type == NodeType.BOOLEAN:
            return self.handle_boolean(node)
        else:
            return node
    # ------------------------------------------------------------------------------------------  
    def handle_program(self, node):
        record = Record(self.settings, '<main>', 'PROGRAM')
        self.settings.initialize_builtin_library(record)
        self.global_memory.stack.push(record)
        return self.evaluate(node.block)
    # ------------------------------------------------------------------------------------------
    def handle_block(self, node):
        none = builtins.objects.Null(self.settings)
        last_value = none._initialize_()
        for instrunction in  node.instructions:
            last_value = self.evaluate(instrunction)
        return last_value
    # ------------------------------------------------------------------------------------------
    def handle_function_definition(self, node):
        """
        A function in reflow formulas can be anonymous or not, in other words you can create functions as:

        >>> function soma(a, b) do
                a + b
            end

        or you can create them anonymously with:

        >>> soma = function(a, b) do
                a + b
            end

        functions, recieving parameters or not MUST be defined with left and right parenthesis so:

        >>> function hello_world() do
                "Hello World"
            end

        Functions, as explained in the '.handle_function_call()' method, are tail call optimized, this means you 
        can loop through each function using recursion. But you sould come up with a solution using a tail call optimized
        solution.

        Args:
            node (reflow_server.formula.utils.parser.nodes.FunctionDefinition): This returns everything needed to create new functions
                                                                                super easy.

        Returns:
            reflow_server.formula.utils.builtins.objects.Function: Return a Function object that can be used to be called later.
        """
        is_anonymous_function = node.variable == None

        function = builtins.objects.Function(self.settings)
        record = self.global_memory.stack.peek()

        parameters = list()
        for parameter in node.parameters:
            if parameter.node_type == NodeType.ASSIGN:
                parameters.append([parameter.left.value.value, self.evaluate(parameter.right)])
            else:
                parameters.append([parameter.value.value, None])

        function = function._initialize_(record, parameters, node.block, self)
        if is_anonymous_function:
            function_name = '<lambda>'
        else:
            function_name = node.variable.value.value
        record.assign(function_name, function)

        return function
    # ------------------------------------------------------------------------------------------
    def handle_module_definition(self, node):
        """
        Similar to Elixir defmodule, a module in Flow language can be a struct or an actual module with static methods.

        A module can be defined as:

        >>> module ModuleName do
                function soma(a, b) do
                    a + b
                end
            end
        
        With this you can access the function 'soma()' with:
        
        >>> ModuleName.soma(1, 2)

        If you want to create a struct with your module you can do this like that:

        >>> module ModuleName(a, b) do
            end

        or simply:

        >>> module ModuleName(a,b)

        Than later you define the struct by doing

        >>> struct_name = ModuleName{a=1, b=2}

        Which you can access the variables by doing like:

        >>> struct_name.a or struct_name.b

        You can also define the values by position like so:
        
        >>> ModuleName{10, 20} 

        Since the first variable is "a", 10 will be assigned to "a", and since the second variable is "b", 20 will be assigned to "b".

        Last but not least, you can create structs and modules like

        >>> module ModuleName(value_a, value_b) do
                function soma(a, b) do
                    a + b
                end
            end
        
        So with this we can create a ModuleName struct with the parameters "value_a" and "value_b", the created struct WILL NOT HAVE ACCESS FOR THE FUNCTIONS 
        OF THE MODULE. When you use "ModuleName.soma()" you WILL NOT BE ABLE TO ACCESS the ModuleName.value_a or ModuleName.value_b

        Args:
            node (reflow_server.formula.utils.parser.nodes.ModuleDefinition): The node responsible for defining the module or struct, with this we can know if 
                                                                              the module is just a module, if it is just a struct or if it is a struct and a module.

        Returns:
            reflow_server.formula.utils.builtins.objects.Module.Module: returns a Module builtin object that can be used to create structs or serves just a module
        """
        module_name = node.variable.value.value
        module = builtins.objects.Module(self.settings)
        record = self.global_memory.stack.peek()

        if node.parameters == None:
            parameters = None
        else:
            parameters = list()
            for parameter in node.parameters:
                if parameter.node_type == NodeType.ASSIGN:
                    parameters.append([parameter.left.value.value, parameter.right])
                else:
                    parameters.append([parameter.value.value, None])


        module = module._initialize_(module_name, record, parameters)

        for module_literal in node.module_literals:
            key_string = builtins.objects.String(self.settings)
            key_string._initialize_(module_literal.variable.value.value)
            module._setattribute_(key_string, module_literal.block)
        
        record.assign(module_name, module)
        return module
    # ------------------------------------------------------------------------------------------
    def handle_function_call(self, node):
        """
        Most of how this works is explained above in the '.evaluate()' function. In simple words the functions are
        tail call optimized.

        Besides that, you can call the function by naming each parameter or by the position on each parameter.

        Args:
            node (reflow_server.formula.utils.parser.nodes.FormulaCall): The formula call node that holds the name of the function 
                                                                         which is not obligatory, and the parameters of the function

        Returns:
            [Function, reflow_server.formula.utils.builtins.objects.*]: Returns a python function to be evaluated later or the actual
                                                                        value of the function.
        """
        # <lambda> is not a valid variable, remember that, so it's ok to add it 
        function_name = node.name.value.value if node.name.node_type == NodeType.VARIABLE else '<lambda>'
        record = self.global_memory.stack.peek()
        function_object = self.evaluate(node.name)
        # ------------------------------------------------------------------------------------------
        def retrieve_function_parameters():
            # Gets the positional parameters and also the values parameters
            # okay so since we can have positional and value parameters the order of the parameters SHOULD NOT MATTER.
            # this might be confusing for some but the idea is simple:
            # We add the parameter in the record that was defined in the call and in the function definition AT THE SAME TIME.
            # There's a catch though, if we are adding the value of a paramater that was defined in the function definition
            # we cannot replace if the value was already added. WHAT?
            # For example: function soma(b=1, a) do....
            # then soma(a=2) 

            # on the first pass we defined both 1 to 'b' and 2 to 'a', on the second pass when we pass through 'a' 
            # we DO NOT assign None to 'a' because we will aready have assigned 'a'.
            parameters = {}
            variable_defined = []
            for index, parameter in enumerate(function_object.parameters):
                if index < len(node.parameters):
                    if node.parameters[index].node_type == NodeType.ASSIGN:
                        parameter_name = node.parameters[index].left.value.value

                        if parameter_name not in function_object.parameters_variables:
                            builtins.objects.Error(self.settings)._initialize_('AttributeError', 'parameter of function "{parameter_name}" is not defined in function'.format(parameter_name=parameter_name))

                        parameter_value = self.evaluate(node.parameters[index].right)
                        parameters[parameter_name] = parameter_value
                        variable_defined.append(parameter_name)
                    else:
                        parameters[parameter[0]] = self.evaluate(node.parameters[index])
                        variable_defined.append(parameter[0])
                if parameter[0] not in variable_defined:
                    if parameter[1] == None:
                        builtins.objects.Error(self.settings)._initialize_('AttributeError', 'parameter "{parameter_name}" was not assigned in the function call'.format(parameter_name=parameter[0]))

                    parameters[parameter[0]] = parameter[1]
                    variable_defined.append(parameter[0])
            return parameters
        # ------------------------------------------------------------------------------------------
        def create_function_record(parameters):
            function_record = Record(self.settings, function_name,'FUNCTION')

            # Define the scope of the function in the new function call stack, this means that
            #
            # variable = 1
            # function test() do  
            #   variable
            # end

            # 'variable' will be available inside of the function even though it was defined outside of the function.
            for key, value in function_object.scope.members.items():
                function_record.assign(key, value)

            for parameter_name, parameter_value in parameters.items():
                function_record.assign(parameter_name, parameter_value)
            return function_record
        # ------------------------------------------------------------------------------------------
        def to_evaluate_function(push_to_current=False):
            """
            This is a function used to evaluate the function, when the function is in a recursion, in order to tail call
            optimize the function call we send this function so we can evaluate it after. The idea is simple, if push_to_current
            is False we push the record to a new stack, otherwise we push the new record to the current record position.

            Args:
                push_to_current (bool, optional): If set to False, we will create a new record in the memory, otherwise we push the record to the current
                                                  record that is running. Defaults to False.

            Returns:
                reflow_server.formula.utils.builtins.objects.*: Returns the actual value, result of the function.
            """
            parameters = retrieve_function_parameters()
            record = create_function_record(parameters)
            if push_to_current:
                self.global_memory.stack.push_to_current(record)
            else:
                self.global_memory.stack.push(record)

            result = function_object._call_(parameters) 
                        
            if push_to_current == False:
                self.global_memory.stack.pop()  
            return result

        # If this condition is set this means we are inside a recursion (we are in a function named fibonacci, and calling it again)
        # we NEED TO DO THIS TO ACCEPT TAIL CALL OPTIMIZATION
        # this is because if we didn't do this we would reach the maximum recursion depth of python. Since we don't want this, we send a function to evaluate the function
        # later. 
        # This is heavily inspired in a technique called trampoline: https://blog.logrocket.com/using-trampolines-to-manage-large-recursive-loops-in-javascript-d8c9db095ae3/
        # or in python: http://vdelia.github.io/functional/trampoline/2015/06/26/trampoline.html

        # When we call the function “.handle_function_call()” we will evaluate the function body. 
        # Pay attention that we call the “.evaluate()“ function again while evaluating this function result. 
        # This means that before returning the result of this call, we will call “.handle_function_call()” again. 
        # And again, and again, for every recursion call. This will reach the maximum recursion depth of the language, in this case, Python.
        # So what we do to solve this? We do not evaluate directly in the function call, we return early the result of ‘.handle_function_call()’, 
        # which will be a function, so with that “.handle_function_call()“ will leave the python call stack and we are free to evaluate the result later
        is_in_recursion = function_name == record.name
        
        if is_in_recursion:
            return to_evaluate_function
        else:
            parameters = retrieve_function_parameters()
            record = create_function_record(parameters)
            self.global_memory.stack.push(record)

            result = function_object._call_(parameters)
            # If the result is a function we evaluate the function in a loop.
            while isinstance(result, types.FunctionType):
                result = result(True)
        
            self.global_memory.stack.pop()
            return result
    # ------------------------------------------------------------------------------------------
    def handle_struct(self, node):
        """
        This work similar to functions, we can set the variable positionaly, so by each position like:
        >>> module StructExample(a, b, c)
        >>> StructExample{1, 2, 3}
        

        we can set the variable by the variable name like:
        >>> StructExample{a=1, b=2, c=3}

        or if the struct has some default values we can set them like:
        >>> module StructExample(a, b=1, c=5)
        >>> StructExample{1} 

        The example above will set 1 to 'a'.

        Args:
            node (reflow_server.formula.utils.parser.nodes.Struct): The struct node for handling structs

        Raises:
            Exception: The argument defined when creating the struct was not defined in the struct
            Exception: An argument was not added in the struct

        Returns:
            reflow_server.formula.utils.builtins.objects.Struct: Returns a struct object, a stuct is an object that is used for
                                                                 holding data. This is used in languages like Go, Elixir, Rust,
                                                                 or C. In languages like Python, Java or others we usually have
                                                                 classes for holding data and methods
        """
        module_object = self.evaluate(node.name, True)

        if module_object.struct_parameters == None:
            raise Exception("Can't create a struct with '{module_name}'. Define it as 'module {module_name}() do ... end' ('...' will be the code inside of your module)".format(module_name=module_object.module_name))

        arguments_and_values = []
        
        # This is similar to a function call, the idea is that the order doesn't matter on named or positional arguments.
        # on python you MUST have first positional arguments and second you can have named arguments. On Flow the idea is different
        # it doesn't matter the order of named or positional arguments.
        variable_defined = []
        for index, parameter in enumerate(module_object.struct_parameters):
            
            if index < len(node.arguments):
                if node.arguments[index].node_type == NodeType.ASSIGN:
                    parameter_name = node.arguments[index].left.value.value

                    if parameter_name not in module_object.stuct_parameters_variables:
                        builtins.objects.Error(self.settings)._initialize_('AttributeError', 'Argument of struct "{parameter_name}" was not defined in struct'.format(parameter_name=parameter_name))

                    parameter_value = self.evaluate(node.arguments[index].right, True)
                    arguments_and_values.append([parameter_name, parameter_value])
                    variable_defined.append(parameter_name)
                else:
                    arguments_and_values.append([parameter[0], self.evaluate(node.arguments[index], True)])
                    variable_defined.append(parameter[0])
            if parameter[0] not in variable_defined:
                if parameter[1] == None:
                    builtins.objects.Error(self.settings)._initialize_('AttributeError', 'Argument "{parameter_name}" was not assigned in the struct'.format(parameter_name=parameter_name))

                arguments_and_values.append([parameter[0], self.evaluate(parameter[1], True)])
                variable_defined.append(parameter[0])

        struct = builtins.objects.Struct(self.settings)
        return struct._initialize_(node.name.value.value, arguments_and_values)
    # ------------------------------------------------------------------------------------------
    def handle_if_statement(self, node):
        """
        The if statement is just simple as it is, it evaluate the exprassion getting it is boolean for Truthy or Falsy values
        And then getting either True or False.
        The else part is optional, we just evaluate it if it exists.

        Args:
            node (reflow_server.formula.utils.parser.nodes.IfStatement): The if statement node to be evaluated with the block, the condition
                                                                         and the else block if exists

        Returns:
            reflow_server.formula.utils.builtins.objects.*: returns the object of the result of the block evaluation
        """
        expression_value = self.evaluate(node.expression, True)
        if expression_value._boolean_()._representation_():
            return self.evaluate(node.block, True)
        elif node.else_statement:
            return self.evaluate(node.else_statement, True)
    # ------------------------------------------------------------------------------------------
    def handle_assign(self, node):
        """
        We can assign a value to a variable by 3 types, by variable, by slice and by attribute.

        The first one is when we do:
        >>> variable = "Assign By Variable"

        The second one is when we do something like:
        >>> dict = {
            "key": [
                1, 2, 3
            ]
        }

        >>> dict["key"][0] = "Assign by slice"

        The third one is when we do:
        >>> module Struct(a, b)

        >>> struct = Struct{a=1, b=2}

        >>> struct.a = "Assign By Attribute"

        You can also add new functions to modules by:
        >>> module Module do
                function defined_on_module() do
                    "This was defined on the module"
                end
            end

        >>> Module.defined_outside_the_module = function() do 
                "This was defined outside of the module"
            end

        >>> Module.defined_outside_the_module() 

        It's important to understand that this WILL NOT OVERRIDE THE FUNCTIONS ALREADY DEFINED. YOU CAN ONLY DEFINE ONCE
        in the MODULE.
        
        Args:
            node (reflow_server.formula.utils.parser.nodes.Assign): The assign node for handling assignments

        Returns:
            reflow_server.formula.utils.builtins.objects.*: returns the object you are assigning to the variable
        """
        variable_value = self.evaluate(node.right, True)

        # if we assign to a normal variable
        if node.left.node_type == NodeType.VARIABLE:
            variable_name = node.left.value.value
        
            record = self.global_memory.stack.peek()
            record.assign(variable_name, variable_value)

        # if we assign to a item in an array
        elif node.left.node_type == NodeType.SLICE:
            # variavel[1] -> left_of_slice is the value relative to 'variavel'
            left_of_slice = node.left 
            slices_stack = []
            # we loop trough all slices so we can interpret stuff like variavel[1][2][0] = "teste"
            # we loop from variavel[1][2][0] to variavel[1][2] to variavel[1] and finish at variavel
            while left_of_slice.node_type == NodeType.SLICE:
                slices_stack.append(self.evaluate(left_of_slice.slice))
                left_of_slice = left_of_slice.left
            # root_list is the actual root of the value, for example: array[0][1] the root is 'array' variable even though we have another array inside of the array
            # so for example in an array like [1, [2, [3]]] the root_list is [1, [2, [3]]] as you might expect
            # if the value on the left is not a variable. Exemple: [1, 2, 3][1] = "Teste" should be acceptable although it does nothing
            if left_of_slice.node_type == NodeType.VARIABLE:
                variable_name = left_of_slice.value.value
                record = self.global_memory.stack.peek()
                root_list = record.get(variable_name)
            else:
                root_list = self.evaluate(left_of_slice)
            
            next_list = None

            # now we loop the other way around, from the root to the leaf, so in the example variavel[1][2][0] = "teste"
            # on the first pass list_to_change will be
            # 1. variavel[1]
            # 2. variavel[1][2] and stop there since variavel[1][2][0] is the actual value we want to change
            # in other words, the list_to_change in the example above is variavel[1][2] (it returns a list)
            while len(slices_stack) > 0:
                list_to_change = root_list if next_list == None else next_list
                index_or_key = slices_stack.pop()
                next_list = list_to_change._getitem_(index_or_key)
        
            list_to_change._setitem_(index_or_key, variable_value)
        elif node.left.node_type == NodeType.ATTRIBUTE:
            struct_object = self.evaluate(node.left.left)
            attribute_right = node.left.right_value
            atribute_left = node.left.operation

            # if attribute is for example struct.c.a = "ola"
            # what we need to do is get the struct of struct.c, and after that get
            # the struct of "a" to assign. It is similar to slice assignment
            while atribute_left.node_type == NodeType.ATTRIBUTE:
                key_string = builtins.objects.String(self.settings)
                key_string._initialize_(attribute_right.value)
                struct_object = struct_object._getattribute_(key_string)

                attribute_right = atribute_left.right_value
                atribute_left = atribute_left.left
            
            key_string = builtins.objects.String(self.settings)
            key_string._initialize_(attribute_right.value)

            struct_object._setattribute_(key_string, variable_value)

        return variable_value
    # ------------------------------------------------------------------------------------------
    def handle_variable(self, node):
        """
        This handles when it encounters a variable, it's important to understand just ONE THING here, that's why
        in assign and other places we DO NOT EVALUATE the variable.

        This gets the actual value of the variable from the stack.

        Args:
            node (reflow_server.formula.utils.parser.nodes.Variable): You probably have understood by now that each of this handle
                                                                      functions have their own node. 

        Returns:
            reflow_server.formula.utils.builtins.objects.*: Returns the value of the variable
        """
        variable_name = node.value.value
        record = self.global_memory.stack.peek()
        return record.get(variable_name)
    # ------------------------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------------------------
    def handle_boolean_operation(self, node):
        value_left = self.evaluate(node.left, True)
        value_right = self.evaluate(node.right, True)

        if node.operation.token_type == TokenType.AND:
            return value_left._and_(value_right)
        elif node.operation.token_type == TokenType.OR:
            return value_left._or_(value_right)
    # ------------------------------------------------------------------------------------------    
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
    # ------------------------------------------------------------------------------------------
    def handle_slice(self, node):
        """
        Slice works everytime you make variable[1] or variable["teste"] or whatever. It is not really
        the same slice of python it just accepts simple values like integers, strings, bool and others.

        For lists it also support negative integers like variable[-1] to get the last value.

        The name slice is just for simplicity.
        
        Args:
            node (reflow_server.formula.utils.parser.nodes.Slice): The slice object is simple, it holds the value inside of the
                                                                   slice and the value of the left of the slice to be evaluated
                       
        Returns:
            reflow_server.formula.utils.builtins.objects.*: Returns whatever value that was in the following item of the dict or array
        """
        slice_value = self.evaluate(node.slice)
        value_left = self.evaluate(node.left)
        return value_left._getitem_(slice_value)
    # ------------------------------------------------------------------------------------------
    def handle_unary_conditional(self, node):
        if node.operation.token_type == TokenType.NOT:
            value = self.evaluate(node.value, True)
            return value._boolean_()._not_()
    # ------------------------------------------------------------------------------------------
    def handle_unary_operation(self, node):
        value = self.evaluate(node.value, True)
        if node.operation.token_type == TokenType.SUM:
            return value._unaryplus_()
        elif node.operation.token_type == TokenType.SUBTRACTION:
            return value._unaryminus_()
    # ------------------------------------------------------------------------------------------
    def handle_attribute(self, node):
        """
        This is kinda tricky but it makes a lot of sense once you understand.
        When you are getting the attribute of a struct you need to evaluate it's value otherwise, if it's a module we DO NOT evaluate it's value

        Okay, besides that how it works? similar to functions actually.

        When you call a module or a struct we append all of it's attributes to the call stack so this way it becomes callable. In other words
        a struct and a module to get attributes from is similar to how we get variables inside the scope of a function.

        Args:
            node (reflow_server.formula.utils.parser.nodes.Attribute): The attribute node to be evaluated

        Returns:
            reflow_server.formula.utils.builtins.objects.*: Returns the evaluated value
        """
        module = self.evaluate(node.left, True)
        module_name = module.module_name if hasattr(module, 'module_name') else '<module>'

        previous_record = self.global_memory.stack.peek()
        module_record = Record(self.settings, module_name, 'MODULE')
        self.global_memory.stack.push(module_record)
        # Define the scope of the module
        for key, value in previous_record.members.items():
            module_record.assign(key, value)

        for index in range(0, len(module.attributes.keys)):
            key = module.attributes.keys[index]
            key_string = builtins.objects.String(self.settings)
            key_string._initialize_(key)
            attribute = module._getattribute_(key_string)
            # with this we can handle structs and modules, if it is a struct, we will return the AST to evaluate later,
            # otherwise we will not evaluate it's value
            if hasattr(attribute, 'node_type'):
                attribute = self.evaluate(attribute, True)
            module_record.assign(key, attribute)

        result = self.evaluate(node.operation, True)
        self.global_memory.stack.pop()
        
        return result
    # ------------------------------------------------------------------------------------------
    def handle_null(self, node):
        null = builtins.objects.Null(self.settings)
        return null._initialize_()
    # ------------------------------------------------------------------------------------------
    def handle_datetime(self, node):
        datetime = builtins.objects.Datetime(self.settings)
        return datetime._initialize_(node.value.value)
    # ------------------------------------------------------------------------------------------
    def handle_string(self, node):
        if helpers.is_string(node.value.value):
            string = builtins.objects.String(self.settings)
            return string._initialize_(node.value.value)
        else:
            builtins.objects.Error(self.settings)._initialize_('SyntaxError', 'Cannot interpret string')
    # ------------------------------------------------------------------------------------------
    def handle_integer(self, node):
        if helpers.is_integer(node.value.value):
            integer = builtins.objects.Integer(self.settings)
            return integer._initialize_(node.value.value)
        else:
            builtins.objects.Error(self.settings)._initialize_('SyntaxError', 'Cannot interpret integer')
    # ------------------------------------------------------------------------------------------
    def handle_list(self, node):
        list_value = builtins.objects.List(self.settings)
        members = []
        for member in node.members:
            members.append(self.evaluate(member))
        return list_value._initialize_(members)
    # ------------------------------------------------------------------------------------------
    def handle_dict(self, node):
        dict_value = builtins.objects.Dict(self.settings)
        members = []
        for member in node.members:
            key = self.evaluate(member[0])
            value = self.evaluate(member[1])
            members.append([key, value])
        return dict_value._initialize_(members)
    # ------------------------------------------------------------------------------------------
    def handle_float(self, node):
        value = node.value.value.replace(self.settings.decimal_point_character, '.')
        if helpers.is_float(value):
            float_value = builtins.objects.Float(self.settings)
            return float_value._initialize_(node.value.value)
        else:
            builtins.objects.Error(self.settings)._initialize_('SyntaxError', 'Cannot interpret float')
    # ------------------------------------------------------------------------------------------
    def handle_boolean(self, node):
        if helpers.is_boolean(node.value.value):
            boolean = builtins.objects.Boolean(self.settings)
            return boolean._initialize_(node.value.value)
        else:
            builtins.objects.Error(self.settings)._initialize_('SyntaxError', 'Cannot interpret boolean')
