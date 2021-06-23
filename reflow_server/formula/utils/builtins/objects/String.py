from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import INTEGER_TYPE, \
    STRING_TYPE


class String(Object):
    def __init__(self, settings):
        super().__init__(STRING_TYPE, settings)

    def _initialize_(self, value):
        self.value = value
        return super()._initialize_()

    def _add_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation + object_representation)
        else:
            return super()._add_(obj)
    
    def _multiply_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation * object_representation)
        else:
            return super()._multiply_(obj)

    def _lessthan_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) < len(object_representation))
        else:
            return super()._lessthan_(obj)
    
    def _lessthanequal_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) <= len(object_representation))
        else:
            return super()._lessthanequal_(obj)
    
    def _greaterthan_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) > len(object_representation))
        else:
            return super()._greaterthan_(obj)

    def _greaterthanequal_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) >= len(object_representation))
        else:
            return super()._greaterthanequal_(obj)

    def _boolean_(self):
        representation = self._representation_()
        if representation == '':
            return super().new_boolean(False)
        else:
            return super().new_boolean(True)
    
    def _representation_(self):
        return str(self.value)
