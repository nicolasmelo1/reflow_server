from reflow_server.formula.utils.builtins.objects.Module import Module
from reflow_server.formula.utils.builtins.objects.String import String
from reflow_server.formula.utils.builtins.objects.Function import Function
from reflow_server.formula.utils.helpers import HashTable

import inspect


class LibModuleFunction(Function):
    def __init__(self, settings, function):
        self.function = function
        super().__init__(settings)
    
    def _call_(self, parameters):
        return self.function(**parameters)


class LibraryFunction:
    def __init__(self, function):
        self.decorated_function = function
        self.decorated_function_name = function.__name__
        self.decorated_function_parameters = []
        for key, value in inspect.signature(function).parameters.items():
            if value.__str__().replace(key, '') == '':
                self.decorated_function_parameters.append([key, None])
            else:
                self.decorated_function_parameters.append([key, value._default])

    def __new__(cls, function):
        return cls(function)

    def get_initialized_function(self, settings, scope):
        function = LibModuleFunction(settings, self.decorated_function)
        function._initialize_(scope, self.decorated_function_parameters)
        return function

def functionmethod(function):
    """
    Okay, so this might not make any sense, actually this is one of the MOST complicated
    parts of Flow (YET). It looks intimidating, and i can see why.

    But let's try to keep it simple for a nice understanding what this is doing:
    1 - First things first, this is a decorator to be used on the functions of your modules. Similar to @staticmethod or @classmethod
    in python.
    2 - This changes the attribute of your class directly. So your classes might have some weird behaviour. For example if inside of 
    the module you make a `print(self.__dict__)` you can see that the function you are decorating might not appear as an attribute of 
    the object.
    3 - This decorator works similarly to `@staticmethod`, this means you don't need the `self` parameter in your function.

    SO HOW THIS WORKS:
    1 - We change the attribute of the class, so if you are decorating the method `teste` with this decorator like
    >>> class HTTP(LibraryModule):
            @functionmethod
            def teste(hello):
                print(hello)
    
    HTTP.teste WILL NOT BE OF TYPE FUNCTION, `HTTP.teste` will be of type `LibraryFunction`. 

    Args:
        function ([type]): [description]

    Returns:
        [type]: [description]
    """
    return LibraryFunction(function)

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
        
        for library_function in self.__class__.__dict__.values():
            if isinstance(library_function, LibraryFunction):
                function_object = library_function.get_initialized_function(self.settings, scope)
                function_name = library_function.decorated_function_name
                attribute_key = String(self.settings)
                self._setattribute_(attribute_key._initialize_(function_name), function_object)
        return self