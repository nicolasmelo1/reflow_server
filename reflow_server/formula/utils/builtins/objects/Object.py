class Object:
    def __init__(self, object_type, settings):
        self.type = object_type
        self.settings = settings

    def new_boolean(self, value):
        from reflow_server.formula.utils.builtins.objects.Boolean import Boolean

        boolean = Boolean(self.settings)
        return boolean._initialize_(value)

    def _initialize_(self):
        return self
    
    def _add_(self, obj):
        raise Exception("Unsuported operation '+' between types {} and {}".format(self.type, obj.type))

    def _subtract_(self, obj):
        raise Exception("Unsuported operation '-' between types {} and {}".format(self.type, obj.type))

    def _divide_(self, obj):
        raise Exception("Unsuported operation '/' between types {} and {}".format(self.type, obj.type))

    def _divide_(self, obj):
        raise Exception("Unsuported operation '/' between types {} and {}".format(self.type, obj.type))

    def _remainder_(self, obj):
        raise Exception("Unsuported operation '%' between types {} and {}".format(self.type, obj.type))

    def _multiply_(self, obj):
        raise Exception("Unsuported operation '*' between types {} and {}".format(self.type, obj.type))

    def _power_(self, obj):
        raise Exception("Unsuported operation '^' between types {} and {}".format(self.type, obj.type))

    def _equals_(self, obj):
        # your first tought might be, why do we need to initialize it everytime
        # and do not put in a constant variable.

        # Everytime we initialize we create a NEW OBJECT, than we pass this object.
        # if we initialized it in a constant, when we use it again
        # the values could have changed.
        TRUE = self.new_boolean(True)
        FALSE = self.new_boolean(False)

        is_equal = obj.type == self.type and \
            obj._representation_() == self._representation_()
        if is_equal:
            return TRUE._boolean_()
        else:
            return FALSE._boolean_()

    def _difference_(self, obj):
        TRUE = self.new_boolean(True),
        FALSE = self.new_boolean(False)

        is_different = obj.type != self.type or \
            obj._representation_() != self._representation_()
        if is_different:
            return TRUE._boolean_()
        else:
            return FALSE._boolean_()
        
    def _lessthan_(self, obj):
        return self.new_boolean(False)
    
    def _lessthanequal_(self, obj):
        is_equal = self._equals_(obj)

        if is_equal._boolean_()._representation_() == True:
            return self.new_boolean(True)
        else:
            return self.new_boolean(False)
    
    def _greaterthan_(self, obj):
        return self.new_boolean(False)

    def _greaterthanequal_(self, obj):
        is_equal = self._equals_(obj)

        if is_equal._boolean_()._representation_() == True:
            return self.new_boolean(True)
        else:
            return self.new_boolean(False)

    def _boolean_(self):
        """
        _boolean_ should ALWAYS return a boolean object, if any other type is returned, a error is thrown.
        """
        return self.new_boolean(False)

    def _not_(self):
        return self.new_boolean(not self._boolean_()._representation_())
    
    def _and_(self, obj):
        is_and = self._boolean_()._representation_() and obj._boolean_()._representation_()
        return self.new_boolean(is_and)
    
    def _or_(self, obj):
        is_or = self._boolean_()._representation_() or obj._boolean_()._representation_()
        return self.new_boolean(is_or)
    
    def _unaryplus_(self):
        raise Exception('Unsuported operand type + for {}'.format(self.type))
    
    def _unaryminus_(self):
        raise Exception('Unsuported operand type - for {}'.format(self.type))
    
    def _representation_(self):
        return self
