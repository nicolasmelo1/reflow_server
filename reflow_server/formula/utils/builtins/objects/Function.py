from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import FUNCTION_TYPE


class Function(Object):
    def __init__(self, settings):
        """
        Yes, in flow language the function is an object, this way you can pass them arround as variables, make callback 
        and all that stuff.
        """
        super().__init__(FUNCTION_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self, scope, parameters=[], function_body_block=None, intepreter=None):
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
            return self.interpreter.evaluate(self.function_body)
        else:
            return super()._call_(parameters)