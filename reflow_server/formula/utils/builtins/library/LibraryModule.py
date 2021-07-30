from reflow_server.formula.utils.builtins.objects.Module import Module
from reflow_server.formula.utils.helpers import HashTable


class LibraryModule(Module):
    def _initialize_(self, module_name, scope, struct_parameters):
        self.module_name = module_name
        self.scope = scope
        self.struct_parameters = struct_parameters
        self.attributes = HashTable()

        self.stuct_parameters_variables = []
        if isinstance(struct_parameters, list):
            for parameter_variable, __ in self.struct_parameters:
                self.stuct_parameters_variables.append(parameter_variable)
                
        return self