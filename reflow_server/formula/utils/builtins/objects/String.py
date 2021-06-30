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
        """
        When the other value is a string we concatenate the strings.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.String.String: Returns a new string object with concatenated values
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation + object_representation)
        else:
            return super()._add_(obj)
    
    def _multiply_(self, obj):
        """
        Similar to int multiplication but the other way around, when the user multiplies a string by an integer we repeat
        the string n times returning a new string.
        
        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.String.String: Either returns a string object or throws an error.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == INTEGER_TYPE:
            response = self.__class__(self.settings)
            return response._initialize_(representation * object_representation)
        else:
            return super()._multiply_(obj)

    def _lessthan_(self, obj):
        """
        Less than on strings only verifies if the length of both strings.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns True or False if the string is less bigger
                                                                          than the other, or passes it to the Object class to verify.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) < len(object_representation))
        else:
            return super()._lessthan_(obj)
    
    def _lessthanequal_(self, obj):
        """
        Less than or equal on strings only verifies if the length of both strings.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns True or False if the string is less or equal bigger
                                                                          than the other, or passes it to the Object class to verify.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) <= len(object_representation))
        else:
            return super()._lessthanequal_(obj)
    
    def _greaterthan_(self, obj):
        """
        Greater than on strings only verifies if the length of both strings.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns True or False if the string length is greater than
                                                                          the other, or passes it to the Object class to verify.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) > len(object_representation))
        else:
            return super()._greaterthan_(obj)

    def _greaterthanequal_(self, obj):
        """
        Greater than or equal on strings only verifies if the length of both strings.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): This object can be of any type

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns True or False if the string length is greater than or equal
                                                                          the other, or passes it to the Object class to verify.
        """
        representation = self._representation_()
        object_representation = obj._representation_()

        if obj.type == STRING_TYPE:
            return super().new_boolean(len(representation) >= len(object_representation))
        else:
            return super()._greaterthanequal_(obj)

    def _boolean_(self):
        """
        Truthy or falsy on strings are: if the string is empty then it is False, otherwise it is True.

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: False if the string is empty and True for everything else
        """
        representation = self._representation_()
        if representation == '':
            return super().new_boolean(False)
        else:
            return super().new_boolean(True)
    
    def _representation_(self):
        return str(self.value)
