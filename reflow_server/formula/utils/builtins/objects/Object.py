class Object:
    def __init__(self, object_type, settings):
        """
        This is an object, it represents every object of reflow formulas.
        Every object, similarly to python will contain some double underscore (or dunder) methods.
     
        Those dunder methods are responsible for handling common behaviour in the program like equals, difference, sum, multiplication,
        and so on.
     
        The idea is that by doing this we take away much of the complexity and the workload of the interpreter function
        and give more power to the builtin object types so they are able to handle itself.
     
        With this we are able to create stuff like 'Hello world'.length (this .length can be a function we call on a atribute of the string type)
        we are able to give more funcionality to the integer, strings, floats and so on.

        The problem is that sometimes stuff can repeat between objects, like Float and Integer share a similar behaviour, but we repeat
        the code on each one.

        Okay, so how does this work?

        When the interpreter finds a binary operation for example (1 + 2) 
        what we do is valueLeft._add_(valueRight). Super simple. If you understand right, 1 will be represented
        as an object `Integer(1)`, so in other words, the REAL value is `Integer(1)._add_(Integer(2))`.
    
        That's the kind of flexibility and achievment we can have by doing stuff like this.
    
        OKAY, but what happens to the ORIGINAL value?

        The original value can be retrieved by calling _representation_(): this is the Python value or the value in whatever language you are using to
        build this interpreter on.
        """
        self.type = object_type
        self.settings = settings
    # ------------------------------------------------------------------------------------------
    def new_boolean(self, value):
        from reflow_server.formula.utils.builtins.objects.Boolean import Boolean

        boolean = Boolean(self.settings)
        return boolean._initialize_(value)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self):
        return self
    # ------------------------------------------------------------------------------------------
    def _in_(self, obj):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "type '{}' is not iterable, so replace {} with a iterable type".format(self.type, obj._representation_()))
    # ------------------------------------------------------------------------------------------
    def _getattribute_(self, variable):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('AttributeError',"Cannot get attribute '{}'".format(variable._representation_(), self.type))
    # ------------------------------------------------------------------------------------------
    def _getitem_(self, item):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('AttributeError', "Cannot get item '{}' of type {}".format(item, self.type))
    # ------------------------------------------------------------------------------------------
    def _setattribute_(self, variable, element):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('AttributeError', "Cannot set attribute '{}' of type {}".format(variable._representation_(), self.type))
    # ------------------------------------------------------------------------------------------
    def _setitem_(self, item, element):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('KeyError', "Cannot set element '{}' at item '{}' of type {}".format(element, item, self.type))
    # ------------------------------------------------------------------------------------------
    def _add_(self, obj):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "Unsuported operation '+' between types {} and {}".format(self.type, obj.type))
    # ------------------------------------------------------------------------------------------
    def _subtract_(self, obj):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "Unsuported operation '-' between types {} and {}".format(self.type, obj.type))
    # ------------------------------------------------------------------------------------------
    def _divide_(self, obj):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "Unsuported operation '/' between types {} and {}".format(self.type, obj.type))
    # ------------------------------------------------------------------------------------------
    def _remainder_(self, obj):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "Unsuported operation '%' between types {} and {}".format(self.type, obj.type))
    # ------------------------------------------------------------------------------------------
    def _multiply_(self, obj):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "Unsuported operation '*' between types {} and {}".format(self.type, obj.type))
    # ------------------------------------------------------------------------------------------
    def _power_(self, obj):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "Unsuported operation '^' between types {} and {}".format(self.type, obj.type))
    # ------------------------------------------------------------------------------------------
    def _equals_(self, obj):
        # your first tought might be, why do we need to initialize it everytime
        # and do not put in a constant variable.

        is_equal = obj.type == self.type and \
            obj._representation_() == self._representation_()
        
        return self.new_boolean(is_equal)
    # ------------------------------------------------------------------------------------------
    def _difference_(self, obj):
        is_different = obj.type != self.type or \
            obj._representation_() != self._representation_()
        return self.new_boolean(is_different)
    # ------------------------------------------------------------------------------------------
    def _lessthan_(self, obj):
        return self.new_boolean(False)
    # ------------------------------------------------------------------------------------------
    def _lessthanequal_(self, obj):
        is_equal = self._equals_(obj)
        return self.new_boolean(is_equal._boolean_()._representation_())
    # ------------------------------------------------------------------------------------------
    def _greaterthan_(self, obj):
        return self.new_boolean(False)
    # ------------------------------------------------------------------------------------------
    def _greaterthanequal_(self, obj):
        is_equal = self._equals_(obj)
        return self.new_boolean(is_equal._boolean_()._representation_())
    # ------------------------------------------------------------------------------------------
    def _boolean_(self):
        """
        _boolean_ should ALWAYS return a boolean object, if any other type is returned, a error is thrown.
        """
        return self.new_boolean(False)
    # ------------------------------------------------------------------------------------------
    def _not_(self):
        return self.new_boolean(not self._boolean_()._representation_())
    # ------------------------------------------------------------------------------------------
    def _and_(self, obj):
        is_and = self._boolean_()._representation_() and obj._boolean_()._representation_()
        return self.new_boolean(is_and)
    # ------------------------------------------------------------------------------------------
    def _or_(self, obj):
        is_or = self._boolean_()._representation_() or obj._boolean_()._representation_()
        return self.new_boolean(is_or)
    # ------------------------------------------------------------------------------------------
    def _unaryplus_(self):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', 'Unsuported operand type + for {}'.format(self.type))
    # ------------------------------------------------------------------------------------------    
    def _unaryminus_(self):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', 'Unsuported operand type - for {}'.format(self.type))
    # ------------------------------------------------------------------------------------------    
    def _representation_(self):
        return self
    # ------------------------------------------------------------------------------------------    
    def _safe_representation_(self):
        return ''
    # ------------------------------------------------------------------------------------------    
    def _hash_(self):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "'{}' is not hashable".format(self.type))
    # ------------------------------------------------------------------------------------------    
    def _length_(self):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "'{}' has no length".format(self.type))
    # ------------------------------------------------------------------------------------------    
    def _call_(self, parameters={}):
        from reflow_server.formula.utils.builtins.objects.Error import Error
        Error(self.settings)._initialize_('Error', "'{}' cannot be called".format(self.type))