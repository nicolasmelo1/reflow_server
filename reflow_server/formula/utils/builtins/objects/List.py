from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import LIST_TYPE
from reflow_server.formula.utils.helpers import DynamicArray


class List(Object):
    def __init__(self, settings):
        super().__init__(LIST_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self, array=[]):
        self.cached_number_of_elements = len(array)
        self.has_to_request_new_representation = True
        self.cached_representation = [element._representation_() for element in array if hasattr(element, '_representation_')]
        
        self.array = DynamicArray(array)        
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _add_(self, obj):
        itens_in_array = [item for item in self.array.array if item is not None]
        if obj.type == LIST_TYPE:
            itens_in_object_array = [item for item in obj.array.array if item is not None]
            
            response = self.__class__(self.settings)
            new_array = itens_in_array + itens_in_object_array
            return response._initialize_(new_array)
        else:
            return super()._add_(obj)
    # ------------------------------------------------------------------------------------------
    def _getitem_(self, index):
        if not isinstance(index, int): 
            index = index._representation_()
        return self.array[index]
    # ------------------------------------------------------------------------------------------
    def _setitem_(self, index, element):
        self.has_to_request_new_representation = True
        return self.array.insert_at(element, int(index._representation_()))
    # ------------------------------------------------------------------------------------------
    def _in_(self, obj):
        return self.new_boolean(obj._representation_() in self.represented_items_in_array)
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        if getattr(self, 'has_to_request_new_representation', True):
            self.cached_representation = [
                self.array[index]._representation_() for index in range(0, self.array.number_of_elements) if hasattr(self.array[index], '_representation_')
            ]
            self.has_to_request_new_representation = False

        return self.cached_representation 
    # ------------------------------------------------------------------------------------------
    def _string_(self, ident=4, **kwargs):
        length = len(self.array)
        stringfied_representation = '[\n'
        for index in range(0, length):
            value_at_index = self.array[index]
            stringfied_value = value_at_index._string_(ident=ident+4)
            value_representation = stringfied_value._representation_()

            stringfied_representation += ' ' * ident + f"{value_representation}" + \
                f"{'' if index == length - 1 else self.settings.positional_argument_separator}\n"
        stringfied_representation += ' ' * (ident-4) if ident - 4 != 1 else '' + ']'
        return self.new_string(stringfied_representation)
    