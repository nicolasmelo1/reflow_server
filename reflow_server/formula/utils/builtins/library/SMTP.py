from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    LibraryStruct


class SMTP(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope, [])
        return self
    
    @functionmethod
    def send_email(self):
        pass