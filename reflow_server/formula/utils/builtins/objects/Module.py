from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import MODULE_TYPE
from reflow_server.formula.utils.helpers import HashTable


class Module(Object):
    def __init__(self, settings):
        super().__init__(MODULE_TYPE, settings)

    def _initialize_(self, module_name, scope, struct_parameters):
        self.module_name = module_name
        self.scope = scope
        self.struct_parameters = struct_parameters
        self.attributes = HashTable()

        self.stuct_parameters_variables = []
        if isinstance(struct_parameters, list):
            for parameter_variable, __ in self.struct_parameters:
                self.stuct_parameters_variables.append(parameter_variable)
                
        return super()._initialize_()

    def _setattribute_(self, variable, element):
        self.attributes.append(variable._hash_(), variable._representation_(), element)

    def _getattribute_(self, variable):
        return self.attributes.search(variable._hash_(), variable._representation_()).value
    
    def _representation_(self):
        return self