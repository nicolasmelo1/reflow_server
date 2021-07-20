from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import STRUCT_TYPE
from reflow_server.formula.utils.helpers import HashTable


class Struct(Object):
    def __init__(self, settings):
        super().__init__(STRUCT_TYPE, settings)

    def _initialize_(self, arguments_and_values):
        from reflow_server.formula.utils.builtins.objects.String import String
        self.attributes = HashTable()
        
        for key, value in arguments_and_values:
            string = String(self.settings)
            string._initialize_(key)
            self.attributes.append(string._hash_(), string._representation_(), value)
        return super()._initialize_()

    def _getattribute_(self, variable):
        return self.attributes.search(variable._hash_(), variable._representation_())
     