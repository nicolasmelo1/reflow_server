from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule
from reflow_server.formula.utils.builtins.objects.String import String
from reflow_server.formula.utils.builtins.objects.Function import Function


class Teste(Function):
    def _call_(self, parameters):
        print('sei la')


class HTTP(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(module_name='HTTP', scope=scope, struct_parameters=[])

        teste = Teste(self.settings)
        teste._initialize_(scope)
        key_teste = String(self.settings)
        self._setattribute_(key_teste._initialize_('teste'), teste)
        return self