from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import DICT_TYPE
from reflow_server.formula.utils.helpers import HashTable


class Dict(Object):
    def __init__(self, settings):
        super().__init__(DICT_TYPE, settings)
    # ------------------------------------------------------------------------------------------    
    def _initialize_(self, values=[]):
        self.values = values
        hashes_keys_and_values = []
        for value in values:
            hashes_keys_and_values.append([value[0]._hash_(), value[0]._representation_(), value[1]])

        self.hash_table = HashTable(hashes_keys_and_values)
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------    
    def _getitem_(self, key):
        """
        Retrieves an item from a key, from the dict. You can also chain those retrievals like ["key1"]["key2"] and so on.

        Args:
            key (
                reflow_server.formula.utils.builtins.objects.Float.Float,
                reflow_server.formula.utils.builtins.objects.Boolean.Boolean,
                reflow_server.formula.utils.builtins.objects.Integer.Integer,
                reflow_server.formula.utils.builtins.objects.String.String
            ): The actual key of the value dict you want to retrieve information from

        Returns:
            reflow_server.formula.utils.builtins.objects.*: Returns the object you were holding in the key value.
        """
        return self.hash_table.search(key._hash_(), key._representation_()).value
    # ------------------------------------------------------------------------------------------    
    def _setitem_(self, key, element):
        """
        Sets an element to a specific key.

        Args:
            key (
                reflow_server.formula.utils.builtins.objects.Float.Float,
                reflow_server.formula.utils.builtins.objects.Boolean.Boolean,
                reflow_server.formula.utils.builtins.objects.Integer.Integer,
                reflow_server.formula.utils.builtins.objects.String.String
            ): The actual key of the value dict you want to retrieve information from
            element (reflow_server.formula.utils.builtins.objects.*): The element you are storing in the dict at the specific key

        Returns:
            reflow_server.formula.utils.builtins.objects.*: Returns the object you are storing in the key value.
        """
        self.values.append([key, element])
        return self.hash_table.append(key._hash_(), key._representation_(), element)
    # ------------------------------------------------------------------------------------------    
    def _in_(self, obj):
        return self.new_boolean(obj._representation_() in self.hash_table.keys)
    # ------------------------------------------------------------------------------------------
    def _subtract_(self, obj):
        """
        Removes a key from the dict.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): The object key you want to remove from the dict.

        Raises:
            Exception: If the key does not exist, raises an error.

        Returns:
            self: returns the actual dict object
        """
        if obj._representation_() in self.hash_table.keys:
            self.hash_table.remove(obj._hash_(), obj._representation_())
            return self
        else:
            raise Exception('Cannot remove {}'.format(obj._representation_()))
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        dictionary_response = {}

        for index in range(0, len(self.hash_table.keys)):
            key = self.hash_table.keys[index]
            key_index = self.hash_table.indexes[index]
            value = self.hash_table.search(key, None, key_index)
            python_value = value.value._representation_()
            dictionary_response[key] = python_value

        return dictionary_response