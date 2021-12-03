from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import FUNCTION_TYPE
from reflow_server.formula.utils.memory import Record

import types


class Function(Object):
    def __init__(self, settings):
        """
        Yes, in flow language the function is an object, this way you can pass them arround as variables, make callback 
        and all that stuff.
        """
        super().__init__(FUNCTION_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self, scope, parameters=[], function_body_block=None, intepreter=None, function_name='<lambda>'):
        self.function_name = function_name
        self.interpreter = intepreter
        self.scope = scope
        self.function_body = function_body_block
        self.parameters = parameters
        self.parameters_variables = []
        for parameter_variable, __ in self.parameters:
            self.parameters_variables.append(parameter_variable)
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        return self
    # ------------------------------------------------------------------------------------------
    def _call_(self, parameters):
        if self.interpreter != None and self.function_body != None:
            def create_function_record(parameters):
                function_record = Record(self.settings, self.function_name, 'FUNCTION')
                # Define the scope of the function in the new function call stack, this means that
                #
                # variable = 1
                # function test() do  
                #   variable
                # end

                # 'variable' will be available inside of the function even though it was defined outside of the function.
                for key, value in self.scope.members.items():
                    function_record.assign(key, self.scope)

                for parameter_name, parameter_value in parameters.items():
                    function_record.assign(parameter_name, parameter_value)
                return function_record
                
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
                record = create_function_record(parameters)
                if push_to_current:
                    self.interpreter.global_memory.stack.push_to_current(record)
                else:
                    self.interpreter.global_memory.stack.push(record)

                result = self.interpreter.evaluate(self.function_body)
                            
                if push_to_current == False:
                    self.interpreter.global_memory.stack.pop()  
                return result
                
            record = self.interpreter.global_memory.stack.peek()

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
            is_in_recursion = self.function_name == record.name
            
            if is_in_recursion:
                return to_evaluate_function
            else:
                record = create_function_record(parameters)
                self.interpreter.global_memory.stack.push(record)

                result = self.interpreter.evaluate(self.function_body)
                # If the result is a function we evaluate the function in a loop.
                while isinstance(result, types.FunctionType):
                    result = result(True)
            
                self.interpreter.global_memory.stack.pop()
                return result
        else:
            return super()._call_(parameters)