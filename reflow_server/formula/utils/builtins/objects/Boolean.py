from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import BOOLEAN_TYPE, \
    FLOAT_TYPE, INTEGER_TYPE 


class Boolean(Object):
    def __init__(self, settings):
        super().__init__(BOOLEAN_TYPE, settings)

    def _initialize_(self, value):
        self.value = value
        return super()._initialize_()
    
    def _boolean_(self):
        return self

    def _lessthan_(self, obj):
        """
        When it's less than we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type
        
        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean: Returns a boolean object representing either True or False for the less than conditional. 
        """

        representation = self._representation_()
        representation = 1 if representation else 0
        object_representation = obj._representation_()
        
        if obj.type in [FLOAT_TYPE, INTEGER_TYPE]:
            return super().new_boolean(representation < object_representation)
        elif obj.type == BOOLEAN_TYPE:
            object_representation = 1 if object_representation else 0
            return super().new_boolean(representation < object_representation)
        else:
            return super()._lessThan_(obj)
    
    def _lessthanequal_(self, obj):
        """
        When it's less than equal we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean: Returns a boolean object representing either True or False for the 
                                                                  less than equal conditional.
        """
        representation = self._representation_()
        representation = 1 if representation else 0
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
            reflow_server.formula.utils.builtins.objects.Boolean: Returns a boolean object representing either True or False for the 
                                                                  greater than conditional.
        """
        representation = self._representation_()
        representation = 1 if representation else 0
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
        When it's grater than equal we convert the boolean representation to either 1 or 0 if the value is a boolean othewise we only
        compare to float or int.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean: Returns a boolean object representing either True or False for the 
                                                                  greater than equal conditional.
        """
        representation = self._representation_()
        representation = 1 if representation else 0
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
        On a boolean, when you write +True, it works like if True was equal 1
        it gives you 1 and if it is +False it is 0

        Returns:
            reflow_server.formula.utils.builtins.objects.Integer.Integer: Returns a new int object with the value 0 or 1
        """
        from reflow_server.formula.utils.builtins.objects.Integer import Integer
        integer = Integer()

        if self._representation_() == True:
            return integer._initialize_(1)
        else:
            return integer._initialize_(0)

    def _unaryminus_(self):
        """
        On a boolean, when you write -True, it works like if True was equal 1
        so it gives you -1 and if it is -False it is 0

        Returns:
            reflow_server.formula.utils.builtins.objects.Integer.Integer: Returns a new int object with the value 0 or -1
        """
        from reflow_server.formula.utils.builtins.objects.Integer import Integer
        integer = Integer()

        if self._representation_() == True:
            return integer._initialize_(-1)
        else:
            return integer._initialize_(0)

    def _representation_(self):
        return bool(self.value)
        