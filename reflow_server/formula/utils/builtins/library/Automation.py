from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

from datetime import datetime


class Automation(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self
    
    @functionmethod
    def trigger_action(data, **kwargs):
        data = retrieve_representation(data)
        
        if isinstance(data, dict) and all([
            isinstance(value, str) or 
            isinstance(value, int) or 
            isinstance(value, bool) or
            isinstance(value, float) or 
            isinstance(value, bytes) or
            isinstance(value, datetime) or 
            value == None 
            for value in data.values()
        ]):
            print(data)

    def _documentation_(self):
        return {}