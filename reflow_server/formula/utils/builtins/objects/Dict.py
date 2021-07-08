from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import DICT_TYPE
from reflow_server.formula.utils.helpers import HashTable


class Dict(Object):
    def __init__(self, settings):
        super().__init__(DICT_TYPE, settings)
    # ------------------------------------------------------------------------------------------    
    def _initialize_(self, values):
        hashes_keys_and_values = []
        for value in values:
            hashes_keys_and_values.append([value[0]._hash_(), value[0]._representation_(), value[1]])

        self.hash_table = HashTable(hashes_keys_and_values)
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------    
    def _getitem_(self, key):
        return self.hash_table.search(key._hash_(), key._representation_()).value
    # ------------------------------------------------------------------------------------------    
    def _setitem_(self, key, element):
        return self.hash_table.append(key._hash_(), key._representation_(), element)