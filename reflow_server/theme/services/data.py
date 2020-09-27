class ThemeReference:
    __FORMULARY_REFERENCE_ERROR_MESSAGE = 'The `formulary_reference` does not exist yet, try adding references with `add_formulary_reference` method.'
    __SECTION_CONDITIONALS_REFERENCE_ERROR_MESSAGE = 'The `section_conditionals_reference` does not exist yet, try adding references with `add_section_conditionals_reference` method.'
    __FIELD_REFERENCE_ERROR_MESSAGE = 'The `field_reference` does not exist yet, try adding references with `add_field_reference` method.'
    __FORM_FIELD_AS_OPTION_ERROR_MESSAGE = 'The `form_field_as_option_reference` does not exist yet, try adding references with `add_form_field_as_option_reference` method.'

    def add_formulary_reference(self, reference_id, instance):
        """
        Adds a new formulary reference. Formulary reference is a dict that holds the reference_id
        as key of the dict and the instance as the value. The reference_id is not the same from the instance.

        If we are adding ThemeForm we hold the Form instance id as `reference_id` and the ThemeForm that was created
        as the instance. On the other hand when creating Form instances it holds the ThemeForm instance id as the `reference_id`
        and the Form instance as the instance.
        
        `formulary_reference` dict is also updated with the sections, SO the `formulary_reference`
        holds the reference on ThemeForm or Form instances, we DO NOT separate between sections and forms.

        This is a dict that holds the reference of ThemeForm and Form instances.

        Args:
            reference_id (int): The id of the object you are referencing.
            instance ((reflow_server.models.formulary.Form, reflow_server.models.theme.ThemeForm)): usually a django 
            model instance. Can be either a Form instance or a ThemeForm instance. It's important that both parameters are inversed:
            if the `reference_id` is the id of a Form instance, this will reciece a ThemeForm instance. If the `reference_id`
            is the id of a ThemeForm instance, this parameter will be a Form instance
        """
        self.formulary_reference = getattr(self, 'formulary_reference', {})
        self.formulary_reference[reference_id] = instance

    def get_formulary_reference(self, reference_id):
        if hasattr(self, 'formulary_reference'):
            return self.formulary_reference[reference_id]
        else:
            raise AttributeError(self.__FORMULARY_REFERENCE_ERROR_MESSAGE)

    def add_section_conditionals_reference(self, reference_id, instance):
        """
        When the section has a conditional, we can't set the conditiona_on_field yet because we 
        haven't created the field just yet. Because of this we create a reference so after we added the 
        fields we can just add the proper conditionals. Each key of the dict is the field_id the conditional 
        references to and the value is the section instance to update.

        This is the same as `formulary_reference` except that is just holds sections (so instances when 
        depends_on IS NOT NULL). These sections are the ones that have a conditional bound to it. The sections
        with conditional_on_field = None ARE NOT on this dict.

        Since this holds the reference of sections, usually the instance will be of type ThemeForm or Form.

        Args:
            reference_id (int): The id of the object you are referencing.
            instance ((reflow_server.models.formulary.Form, reflow_server.models.theme.ThemeForm)): usually a django 
            model instance. Can be either a Form instance or a ThemeForm instance.
        """
        self.section_conditionals_reference = getattr(self, 'section_conditionals_reference', {})
        self.section_conditionals_reference[reference_id] = instance

    def get_section_conditionals_reference(self):
        """
        Returns the `section_conditionals_reference` as a list of tuples

        Raises:
            AttributeError: If the `formulary_reference` haven't been set
            AttributeError: If you haven't added anything on `section_conditionals_reference` dict

        Returns:
            list(tuple): list of tuples, where the first item of the tuple is the field_id and the second item is the instance
        """
        if not hasattr(self, 'formulary_reference'):
            raise AttributeError(self.__FORMULARY_REFERENCE_ERROR_MESSAGE)
        else:
            if hasattr(self, 'section_conditionals_reference'):
                return self.section_conditionals_reference.items()
            else:
                raise AttributeError(self.__SECTION_CONDITIONALS_REFERENCE_ERROR_MESSAGE)

    def add_field_reference(self, reference_id, instance):
        """
        Adds a dict to be used as reference. With this we can know by the ThemeField or Field id what Field or ThemeField
        should we use when we create a new data. On this dict, each key is the ThemeField or Field id, and the value 
        is each Field or ThemeField instance created, respectively. This way whenever we encounter a ThemeField or a Field we 
        can get the Field or ThemeField instance it references to.

        With this we can know for example by the ThemeField id what Field should we use when we create a new data.
        For example, on NotificationConfigurations (not the Theme ones), they are usually bound to a Field instance.
        ThemeNotificationConfiguration holds the reference for a ThemeField. When we are creating a new NotificationConfiguration
        for the user based on the ThemeNotificationConfiguration we will have initally the ThemeField id. We use this
        to set the correct reference to it. The same applies to the opposite order (when we a creating ThemeNotificationConfiguration).

        Args:
            reference_id (int): The id of the object you are referencing.
            instance ((reflow_server.models.formulary.Field, reflow_server.models.theme.ThemeField)): usually a django 
            model instance. Can be either a Field instance or a ThemeField instance. It's important that both parameters are inversed:
            if the `reference_id` is the id of a Field instance, this will reciece a ThemeField instance. If the `reference_id`
            is the id of a ThemeField instance, this parameter will be a Field instance
        """
        self.field_reference = getattr(self, 'field_reference', {})
        self.field_reference[reference_id] = instance

    def get_field_reference(self, reference_id):
        if not hasattr(self, 'formulary_reference'):
            raise AttributeError(self.__FORMULARY_REFERENCE_ERROR_MESSAGE)
        else:
            if hasattr(self, 'field_reference'):
                return self.field_reference[reference_id]
            else:
                raise AttributeError(self.__FIELD_REFERENCE_ERROR_MESSAGE)
    