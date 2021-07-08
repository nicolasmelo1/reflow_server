from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import MODULE_TYPE


class Module(Object):
    def __init__(self, settings):
        super().__init__(MODULE_TYPE, settings)
