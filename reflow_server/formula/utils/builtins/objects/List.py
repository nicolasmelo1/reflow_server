from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import LIST_TYPE
from reflow_server.formula.utils.helpers import DynamicArray


class List(Object):
    def __init__(self, settings):
        super().__init__(LIST_TYPE, settings)

    def _initialize_(self, array=[]):
        self.array = DynamicArray(array)
        return super()._initialize_()
    
    def _add_(self, obj):
        itens_in_array = [item for item in self.array.array if item is not None]
        if obj.type == LIST_TYPE:
            itens_in_object_array = [item for item in obj.array.array if item is not None]
            
            response = self.__class__(self.settings)
            new_array = itens_in_array + itens_in_object_array
            return response._initialize_(new_array)
        else:
            return super()._add_(obj)

    def _getitem_(self, index):
        return self.array[int(index)]
    
    def _setitem_(self, index, element):
        return self.array.insert_at(element, int(index))

    def _representation_(self):
        to_show = []
        for element in self.array.array:
            if hasattr(element, '_representation_'):
                to_show.append(element._representation_())
        return to_show
    