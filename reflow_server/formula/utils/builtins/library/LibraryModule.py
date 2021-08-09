from reflow_server.formula.utils.builtins.objects.Module import Module
from reflow_server.formula.utils.builtins.objects.String import String
from reflow_server.formula.utils.builtins.objects.Function import Function
from reflow_server.formula.utils.builtins.objects.Struct import Struct
from reflow_server.formula.utils.helpers import HashTable, Conversor

import inspect


class LibraryFunction(Function):
    """
    An extended and different Function object, the idea is super simple,
    the only difference from this and the original Function class is that
    this one also recieves the `function` parameter, so we have the referece
    for the function we decorated with `functionmethod` decorator.
    """
    def __init__(self, settings, function, parameters_context):
        self.parameters_context = {value:key for key, value in parameters_context.items()}
        self.function = function
        super().__init__(settings)
    
    def _call_(self, parameters):
        """
        When we call the function we also pass the settings in a special __settings__ parameter.
        """
        # in order to call the function we have to convert the translated attribute
        # to the original attribute so it doesn't throw any error. For example if we translated
        # 'url' to 'endereco' the attribute is 'endereco' and not 'url'. So we need to traslate from 
        # 'endereco' back to 'url'
        function_parameters = {}
        function_parameters['__settings__'] = self.settings
        for key in parameters.keys():
            function_parameters[self.parameters_context.get(key, key)] = parameters[key]
        return self.function(**function_parameters)


class LibraryFunctionHelper:
    def __init__(self, function):
        self.decorated_function = function
        self.decorated_function_name = function.__name__

    def get_initialized_function(self, settings, module_name, scope):
        """
        Retrieves the actual function class, this is used to add the function as an attribute of a module.

        Args:
            settings (reflow_server.formula.utils.settings.Setting): This is the settings instance so we can translate the formula
                                                                     but also know other stuff about the user who is running the 
                                                                     formula.
            module_name (str): The name of the module where this function is set, this is the ORIGINAL name and not
                               the translated one.
            scope (reflow_server.formula.utils.memory.Record): The record instance so we can have access of all
                                                               of the variables.

        Returns:
            reflow_server.formula.utils.builtins.library.LibraryModule.LibraryFunction: Returns a new special Function instance.
        """
        # This is responsible for translating the attribute parameters of the function in real time.
        context_module = settings.library.get(module_name, None)

        parameters_context_translation_reference = getattr(
            getattr(
                context_module, 
                'methods', 
                {}
            ).get(self.decorated_function_name, None), 
            'parameters', 
            {}
        )

        decorated_function_parameters = []
        for key, value in inspect.signature(self.decorated_function).parameters.items():
            translated_parameter_name = parameters_context_translation_reference.get(key, key)
            if value.__str__().replace(key, '') == '':
                decorated_function_parameters.append([translated_parameter_name, None])
            else:
                decorated_function_parameters.append([translated_parameter_name, value._default])

        function = LibraryFunction(settings, self.decorated_function, parameters_context_translation_reference)
        function._initialize_(scope, decorated_function_parameters)
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
    
    HTTP.teste WILL NOT BE OF TYPE FUNCTION, `HTTP.teste` will be of type `LibraryFunctionHelper`. 
    2 - Since we are decorating if we do `print(function)` you will see that `function` is an object of type function, this is the original
    callable function
    3 - We pass this original function then to the LibraryFunctionHelper object. The LibraryFunctionHelper is just a helper object, 
    we will explain it later why this IS NOT a reflow_server.formula.utils.builtins.objects.Function instance.

    4-On the `._initialize_` method in the LibraryModule class we then initialize the actual Function object.
    on this Function object we pass the original decorated function.
    
    When we run the `_call_()` method of the function we then pass all of the parameters to the function 
    we decorated, so in other words, we just run the actual function we decorated.

    Args:
        function (function): This is the python function object.

    Returns:
        reflow_server.formula.utils.builtins.library.LibraryModule.LibraryFunctionHelper: The helper object used as a factory to generate
                                                                                          Function instances.
    """
    return LibraryFunctionHelper(function)


class LibraryModule(Module):
    def _initialize_(self, scope, struct_parameters):
        module_name = self.__class__.__name__
        context_module = self.settings.library.get(module_name, None)

        self.module_name = getattr(context_module, 'module_name', module_name)
        self.scope = scope
        self.struct_parameters = struct_parameters
        self.attributes = HashTable()

        self.stuct_parameters_variables = []
        if isinstance(struct_parameters, list):
            for parameter_variable, __ in self.struct_parameters:
                parameter_variable_name = getattr(context_module, 'struct_parameters', {}).get(parameter_variable, parameter_variable)
                self.stuct_parameters_variables.append(parameter_variable_name)
        
        # we look for LibraryFunctionHelper instances DIRECTLY IN THE CLASS, NOT THE INSTANCE
        # with this we initialize the actual function.
        for library_function in self.__class__.__dict__.values():
            if isinstance(library_function, LibraryFunctionHelper):
                function_object = library_function.get_initialized_function(self.settings, module_name, scope)
                original_function_name = library_function.decorated_function_name
                function_name = getattr(getattr(context_module, 'methods', {}).get(original_function_name, None), 'method_name', original_function_name)
                attribute_key = String(self.settings)
                self._setattribute_(attribute_key._initialize_(function_name), function_object)
        return self
    
    
class LibraryStruct(Struct):
    """
    This class is responsible for creating structs, super simple actually.

    You might be asking yourself how e transform something in a struct and how do we know which arguments to use?
    
    For example:
    >>> class HTTPResponse(LibraryStruct):
            def __init__(self, settings, response, decode_format='utf-8'):
                self.status_code = response.code
                self.content = response.read().decode(decode_format)
                try:
                    self.json = json.loads(self.content)
                except Exception as e:
                    self.json = None
                super().__init__(settings)

    everything mapped to the object is translated as a attribute, so self.status_code maps to `status_code`.
    self.content is mapped to `content` attribute, and last but not least self.json maps to `json` attribute.

    Have you seen a pattern here? self.xpto = 'hey' will be mapped to `xpto` attribute in the HTTPResponse struct.

    So how to NOT pass attributes here? Simple, just don't add an attribute to `self`, otherwise you can just use the
    'attributes_to_ignore' list passing the string of each attribute YOU DON'T WANT TO BE AVAILABLE IN YOUR STRUCT

    WARNING:
    for attributes "private" attributes like "self.__response" for example, python does a name mangling like _HTTPResponse__response
    so we need to be aware of those. We automatically evaluate this to ignore so you don't need to worry
    """
    def __init__(self, module_name, settings, attributes_to_ignore=[]):
        super().__init__(settings)
        original_struct_name = self.__class__.__name__
        # makes the translation
        context_module = self.settings.library.get(module_name, None)
        context_struct = getattr(context_module, 'structs', {}).get(original_struct_name, None)
        struct_name = getattr(
            context_struct, 
            'struct_name', 
            original_struct_name
        )

        arguments_and_values = []
        conversor = Conversor(settings)

        private_attributes_to_ignore = [f"_{self.__class__.__name__}{attribute_to_ignore}" for attribute_to_ignore in attributes_to_ignore]
        attributes_to_ignore = attributes_to_ignore + private_attributes_to_ignore
        
        for key, value in self.__dict__.items():
            # type and settings are ignored because they are defined in the reflow_server.formula.utils.builtins.objects.Object object.
            if key not in attributes_to_ignore and key not in ['type', 'settings']:
                attribute_name = getattr(context_struct, 'attributes', {}).get(key, key)
                arguments_and_values.append([attribute_name, conversor.python_value_to_flow_object(value)])

        self._initialize_(struct_name, arguments_and_values)
        