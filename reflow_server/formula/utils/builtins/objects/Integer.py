from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import BOOLEAN_TYPE, \
    FLOAT_TYPE, INTEGER_TYPE, STRING_TYPE


class Integer(Object):
    def __init__(self, settings):
        super().__init__(INTEGER_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self, value):
        self.value = value
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _add_(self, obj):
        """
        On integers we can only add between Floats or Integers, when adding by an integer, 
        returns an integer, otherwise returns a float.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            Tuple[
                reflow_server.formula.utils.builtins.objects.Integer.Integer, 
                reflow_server.formula.utils.builtins.objects.Float.Float
            ]: Returns either a float when adding by floats or a int
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float
            
            response = Float(self.settings)
            return response._initialize_(representation + object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation + object_representation)
        else:
            return super()._add_(obj)
    # ------------------------------------------------------------------------------------------
    def _subtract_(self, obj):
        """
        On integers we can only subtract from another integer or another float, other types are unsuported. When subtracting
        by an float always return a float.
        
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            Tuple[
                reflow_server.formula.utils.builtins.objects.Integer.Integer, 
                reflow_server.formula.utils.builtins.objects.Float.Float
            ]: Returns either a float when subtracting by floats or a int
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float
            
            response = Float(self.settings)
            return response._initialize_(representation - object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation - object_representation)
        else:
            return super()._subtract_(obj)
    # ------------------------------------------------------------------------------------------
    def _multiply_(self, obj):
        """
        Multiplication with integers are supported between string, float or other ints, all other types are unsuported.
        When the user multiplies a string with an int we repeat the string n times, returning a new string object,
        When the user multiplies with a float we return a new float object, as it should be expected.
        Last but not least when the user multiplies with int we return a new object of type int with the newly created value.
        
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            Tuple[
                reflow_server.formula.utils.builtins.objects.Integer.Integer, 
                reflow_server.formula.utils.builtins.objects.Float.Float,
                reflow_server.formula.utils.builtins.objects.String.String
            ]: Returns either a float when multiplying by floats, a int, or a string repeated n times.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            from reflow_server.formula.utils.builtins.objects.String import String
            
            response = String(self.settings)
            return response._initialize_(object_representation * representation)
        elif obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float
            
            response = Float(self.settings)
            return response._initialize_(representation * object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation * object_representation)
        else:
            return super()._multiply_(obj)
    # ------------------------------------------------------------------------------------------
    def _divide_(self, obj):
        """
        You can either divide by an integer or by a float, also remember, you can't divide by 0
        
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            Tuple[
                reflow_server.formula.utils.builtins.objects.Integer.Integer, 
                reflow_server.formula.utils.builtins.objects.Float.Float
            ]: Returns either a float when dividing by floats or a int
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            if float(object_representation) == 0:
                from reflow_server.formula.utils.builtins.objects.Error import Error
                Error(self.settings)._initialize_('Error', 'Cannot divide by 0')
            elif obj.type == FLOAT_TYPE:
                from reflow_server.formula.utils.builtins.objects.Float import Float

                response = Float(self.settings)
                return response._initialize_(representation / object_representation)
            else:
                response = self.__class__(self.settings)
                return response._initialize_(representation / object_representation)
        else:
            return super()._divide_(obj)
    # ------------------------------------------------------------------------------------------
    def _remainder_(self, obj):
        """
        You can either retrieve the remainder of an integer or of a float, also remember, you can't divide by 0
        
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            Tuple[
                reflow_server.formula.utils.builtins.objects.Integer.Integer, 
                reflow_server.formula.utils.builtins.objects.Float.Float
            ]: Returns either a float when retrieving the remainder by floats or a int
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            if float(object_representation) == 0:
                from reflow_server.formula.utils.builtins.objects.Error import Error
                Error(self.settings)._initialize_('Error', 'Cannot divide by 0')
            elif obj.type == FLOAT_TYPE:
                from reflow_server.formula.utils.builtins.objects.Float import Float

                response = Float(self.settings)
                return response._initialize_(representation % object_representation)
            else:
                response = self.__class__(self.settings)
                return response._initialize_(representation % object_representation)
        else:
            return super()._remainder_(obj)
    # ------------------------------------------------------------------------------------------
    def _power_(self, obj):
        """
        Really similar to add or subtract, power is only available between ints and floats, other types are not supported        
        
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            Tuple[
                reflow_server.formula.utils.builtins.objects.Integer.Integer, 
                reflow_server.formula.utils.builtins.objects.Float.Float
            ]: Returns the power of either a float or a int
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == FLOAT_TYPE:
            from reflow_server.formula.utils.builtins.objects.Float import Float

            response = Float(self.settings)
            return response._initialize_(representation ** object_representation)
        elif obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation ** object_representation)
        else:
            return super()._power_(obj)
    # ------------------------------------------------------------------------------------------
    def _boolean_(self):
        """
        For truthy or Falsy values in ints, if the value is 0 then it is represented as False, otherwise it is represented
        as True.

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or False
        """
        representation = self._representation_()
        if representation == 0:
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

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation < object_representation)
        else:
            return super()._lessthan_(obj)
    # ------------------------------------------------------------------------------------------
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

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation <= object_representation)
        else:
            return super()._lessthanequal_(obj)
    # ------------------------------------------------------------------------------------------
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

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation > object_representation)
        else:
            return super()._greaterthan_(obj)
    # ------------------------------------------------------------------------------------------
    def _greaterthanequal_(self, obj):
        """
        When it's greater than equal we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.
        
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the greater than equal conditional.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type in [FLOAT_TYPE, INTEGER_TYPE, BOOLEAN_TYPE]:
            if obj.type == BOOLEAN_TYPE:
                object_representation = 1 if object_representation else 0
            return super().new_boolean(representation >= object_representation)
        else:
            return super()._greaterthanequal_(obj)
    # ------------------------------------------------------------------------------------------
    def _unaryplus_(self):
        """
        Returns the positive representation of the particular number

        Returns:
            reflow_server.formula.utils.builtins.objects.Integer.Integer: Returns a new integer object with the positive value of the number
        """
        response = self.__class__(self.settings)
        return response._initialize_(+self._representation_())
    # ------------------------------------------------------------------------------------------
    def _unaryminus_(self):
        """
        Returns the negative representation of the particular number

        Returns:
            reflow_server.formula.utils.builtins.objects.Integer.Integer: Returns a new integer object with the negative value of the number
        """
        response = self.__class__(self.settings)
        return response._initialize_(-self._representation_())
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        return int(self.value)
    # ------------------------------------------------------------------------------------------
    def _string_(self, **kwargs):
        representation = self._representation_()
        return self.new_string(str(representation))
    # ------------------------------------------------------------------------------------------
    def _safe_representation_(self):
        return int(self.value)
    # ------------------------------------------------------------------------------------------
    def _hash_(self):   
        return int(self.value)