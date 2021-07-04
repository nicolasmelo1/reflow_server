from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import FUNCTION_TYPE


class Function(Object):
    def __init__(self, settings):
        super().__init__(FUNCTION_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self, ast_function, scope, parameters):
        self.scope = scope
        self.ast_function = ast_function
        self.parameters = parameters
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        return None