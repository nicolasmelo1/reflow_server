from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod
from reflow_server.formula.utils.builtins.objects.String import String
from reflow_server.formula.utils.builtins.objects.Function import Function


class HTTP(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(module_name='HTTP', scope=scope, struct_parameters=[])
        return self
    
    @functionmethod
    def get(url):
        print(url)