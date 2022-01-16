from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import ERROR_TYPE


class Error(Object, Exception):
    def __init__(self, settings):
        super().__init__(ERROR_TYPE, settings)

    def _initialize_(self, error_type, message):
        self.error_type = error_type
        self.message = message
        raise self
    
    def _representation_(self):
        return f"{self.error_type}: {self.message}"
    
    def _string_(self, **kwargs):
        return self.new_string(f"({self.error_type}): {self.message}")
