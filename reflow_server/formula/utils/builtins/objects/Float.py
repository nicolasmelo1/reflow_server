from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import BOOLEAN_TYPE, FLOAT_TYPE, INTEGER_TYPE


class Float(Object):
    def __init__(self, settings):
        super().__init__(FLOAT_TYPE, settings)
    # ------------------------------------------------------------------------------------------    
    def _initialize_(self, value):
        self.value = value
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _add_(self, obj):
        """
        Similar to subtraction always return a float if you are either adding by int or float

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of many types

        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Always returns a float when working with floats
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            response = self.__class__(self.settings)
            return response._initialize_(representation + object_representation)
        else:
            return super()._add_(obj)
    # ------------------------------------------------------------------------------------------
    def _subtract_(self, obj):
        """
        Similar to Multiply and Divide, always return a float if you are either subtracting by int or float
    
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of many types

        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Always returns a float when working with floats
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            response = self.__class__(self.settings)
            return response._initialize_(representation - object_representation)
        else:
            return super()._subtract_(obj)
    # ------------------------------------------------------------------------------------------
    def _multiply_(self, obj):
        """
        You can either multiply by an integer or by a float.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of many types

        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Always returns a float when working with floats
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            response = self.__class__(self.settings)
            return response._initialize_(representation * object_representation)
        else:
            return super()._multiply_(obj)
    # ------------------------------------------------------------------------------------------
    def _divide_(self, obj):
        """
        You can either divide by an integer or by a float, also remember, you can't divide by 0. Always return a float.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of many types

        Raises:
            Exception: Cannot divide by 0

        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Always returns a float when working with floats
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            if (int(object_representation) == 0):
                raise Exception('Cannot divide by 0')
            else:
                response = self.__class__(self.settings)
                return response._initialize_(representation / object_representation)
        else:
            return super()._divide_(obj)
    # ------------------------------------------------------------------------------------------
    def _remainder_(self, obj):
        """
        You can either divide by an integer or by a float, also remember, you can't divide by 0. Always return a float.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of many types

        Raises:
            Exception: Cannot divide by 0

        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Always returns a float when working with floats
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            if (int(object_representation) == 0):
                raise Exception('Cannot divide by 0')
            else:
                response = self.__class__(self.settings)
                return response._initialize_(representation % object_representation)
        else:
            return super()._remainder_(obj)
    # ------------------------------------------------------------------------------------------
    def _power_(self, obj):
        """
        Similar to add, subtract, and others, always returns a float and can be either done between Floats or Integers

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of many types

        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Returns a float with the power of both values
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            response = self.__class__(self.settings)
            return response._initialize_(representation ** object_representation)
        else:
            return super()._power_(obj)
    # ------------------------------------------------------------------------------------------
    def _boolean_(self):
        """
        Really similar to int boolean. The truthy or falsy works basically the same, when the value is 0.0 or 0.00 or whatever
        we convert this value representation to integer and checks if it's 0, if it is then it's false, otherwise it's true.
    
        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean value representing either True or either False
        """
        representation = self._representation_()
        if int(representation) == 0:
            return super().new_boolean(False)
        else:
            return super().new_boolean(True)
    # ------------------------------------------------------------------------------------------
    def _equals_(self, obj):
        """
        When it's equals we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int. We also convert the float to integer so 1.0 is equal to 1

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the equals conditional. 
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            return super().new_boolean(int(representation) == int(object_representation))
        elif obj.type == BOOLEAN_TYPE:
            object_representation = 1 if object_representation else 0
            return super().new_boolean(int(representation) == int(object_representation))
        else:
            return super()._equals_(obj)
    # ------------------------------------------------------------------------------------------
    def _lessthan_(self, obj):
        """
        When it's less than we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the less than conditional. 
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            return super().new_boolean(representation < object_representation)
        elif obj.type == BOOLEAN_TYPE:
            object_representation = 1 if object_representation else 0
            return super().new_boolean(representation < object_representation)
        else:
            return super()._lessthan_(obj)

    def _lessthanequal_(self, obj):
        """
        When it's less than equal we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the less than equal conditional.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            return super().new_boolean(representation <= object_representation)
        elif obj.type == BOOLEAN_TYPE:
            object_representation = 1 if object_representation else 0
            return super().new_boolean(representation <= object_representation)
        else:
            return super()._lessthanequal_(obj)

    def _greaterthan_(self, obj):
        """
        When it's grater than we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the greater than conditional.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            return super().new_boolean(representation > object_representation)
        elif obj.type == BOOLEAN_TYPE:
            object_representation = 1 if object_representation else 0
            return super().new_boolean(representation > object_representation)
        else:
            return super()._greaterthan_(obj)

    def _greaterthanequal_(self, obj):
        """
        When it's greater than equal we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or False 
                                                                          for the greater than equal conditional.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            return super().new_boolean(representation >= object_representation)
        elif obj.type == BOOLEAN_TYPE:
            object_representation = 1 if object_representation else 0
            return super().new_boolean(representation >= object_representation)
        else:
            return super()._greaterthan_(obj)

    def _unaryplus_(self):
        """
        Returns the positive representation of the particular number

        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Returns a new float object with the positive value of the number
        """
        response = self.__class__(self.settings)
        return response._initialize_(+self._representation_())
    
    def _unaryminus_(self):
        """
        Returns the negative representation of the particular float number
        
        Returns:
            reflow_server.formula.utils.builtins.objects.Float.Float: Returns a new float object with the negative value of the number
        """
        response = self.__class__(self.settings)
        return response._initialize_(-self._representation_())

    def _representation_(self):
        return float(self.value)
