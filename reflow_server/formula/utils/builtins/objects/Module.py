from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import MODULE_TYPE
from reflow_server.formula.utils.helpers import HashTable


class Module(Object):
    def __init__(self, settings):
        super().__init__(MODULE_TYPE, settings)

    def _initialize_(self, module_name, scope):
        self.module_name = module_name
        self.scope = scope
        self.attributes = HashTable()
        return super()._initialize_()

    def _setattribute_(self, variable, element):
        self.attributes.append(hash(variable), variable, element)

    def _getattribute_(self, variable):
        return self.attributes.search(hash(variable), variable)
    
    def _representation_(self):
        return self