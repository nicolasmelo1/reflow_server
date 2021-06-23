from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import BOOLEAN_TYPE, \
    FLOAT_TYPE, INTEGER_TYPE, STRING_TYPE


class Integer(Object):
    def __init__(self, settings):
        super().__init__(INTEGER_TYPE, settings)

    def _initialize_(self, value):
        self.value = value
        return super()._initialize_()
    
    def _add_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float
            
            response = Float()
            return response._initialize_(representation + object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation + object_representation)
        else:
            return super()._add_(obj)

    def _subtract_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float
            
            response = Float()
            return response._initialize_(representation - object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation - object_representation)
        else:
            return super()._subtract_(obj)

    def _multiply_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            from reflow_server.formula.utils.builtins.objects.String import String
            
            response = String()
            return response._initialize_(object_representation * representation)
        elif obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float
            
            response = Float()
            return response._initialize_(representation * object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation * object_representation)
        else:
            return super()._multiply_(obj)

    def _divide_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            if int(object_representation) == 0:
                raise Exception('Cannot divide by 0')
            elif obj.type == FLOAT_TYPE:
                from reflow_server.formula.utils.builtins.objects.Float import Float

                response = Float()
                return response._initialize_(representation / object_representation)
            else:
                response = self.__class__(self.settings)
                return response.__initialize__(representation / object_representation)
        else:
            return super()._divide_(obj)

    def _remainder_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            if int(object_representation) == 0:
                raise Exception('Cannot divide by 0')
            elif obj.type == FLOAT_TYPE:
                from reflow_server.formula.utils.builtins.objects.Float import Float

                response = Float()
                return response._initialize_(representation % object_representation)
            else:
                response = self.__class__(self.settings)
                return response.__initialize__(representation % object_representation)
        else:
            return super()._remainder_(obj)

    def _power_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float

            response = Float()
            return response._initialize_(representation ** object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response.__initialize__(representation ** object_representation)
        else:
            return super()._power_(obj)


    def _boolean_(self):
        representation = self._representation_()
        if representation == 0:
            return super().new_boolean(False)
        else:
            return super().new_boolean(True)

    def _lessthan_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation < object_representation)
        else:
            return super()._lessthan_(obj)

    def _lessthanequal_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation <= object_representation)
        else:
            return super()._lessthanequal_(obj)

    def _greaterthan_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation > object_representation)
        else:
            return super()._greaterthan_(obj)
    
    def _greaterthanequal_(self, obj):
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation >= object_representation)
        else:
            return super()._greaterthanequal_(obj)

    def _unaryplus_(self):
        response = self.__class__(self.settings)
        return response._initialize_(+self._representation_())

    def _unaryminus_(self):
        response = self.__class__(self.settings)
        return response._initialize_(-self._representation_())

    def _representation_(self):
        return int(self.value)