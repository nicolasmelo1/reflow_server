from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import STRUCT_TYPE


class Struct(Object):
    def __init__(self, settings):
        super().__init__(STRUCT_TYPE, settings)

    def _initialize_(self, arguments_and_values):
        return super()._initialize_()