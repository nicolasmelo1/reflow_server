from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import STRUCT_TYPE
from reflow_server.formula.utils.helpers import HashTable


class Struct(Object):
    def __init__(self, settings):
        super().__init__(STRUCT_TYPE, settings)

    def _initialize_(self, module_name, arguments_and_values):
        """
        A struct is similar to an object, except it's way simpler without polymorphism and all of that stuff.

        Args:
            module_name (str): The name of the module that this struct is based on.
            arguments_and_values (list[list[str, any]]): A list of lists, where the first element of the list inside a list
                                                         is a string and the second can be of any type

        Returns:
            self: Returns the actual object
        """
        from reflow_server.formula.utils.builtins.objects.String import String
        self.attributes = HashTable()
        self.module_name = module_name

        for key, value in arguments_and_values:
            string = String(self.settings)
            string._initialize_(key)
            self.attributes.append(string._hash_(), string._representation_(), value)
        return super()._initialize_()

    def _getattribute_(self, variable):
        """
        Similar to Dicts, we hold the values of the attributes
        """
        return self.attributes.search(variable._hash_(), variable._representation_()).value
     
    def _setattribute_(self, variable, element):
        return self.attributes.append(variable._hash_(), variable._representation_(), element)