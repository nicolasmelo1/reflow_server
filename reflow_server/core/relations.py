from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class ValueField(serializers.Field):
    default_error_messages = {
        'blank': _('blank'),
        'too_long': _('too_long'),
    }
    initial = ''

    def __init__(self, **kwargs):
        # In certain use cases i want to be able to load the id, in others i don't, i want to retrieve only the string it references to.
        self.load_ids = kwargs.pop('load_ids', False)
        # This configuration is used to use the FormValue states (check reflow_server/formulary/models/abstracts.py for further explanation)
        # When set to false it means you actually want to use the field state and not the form_value state.
        # we usually only set this to False when we are loading the data of a SPECIFIC/SINGLE form for the user to edit, otherwise we use always 
        # the FormValue state.
        self.use_state = kwargs.pop('use_state', True)
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.max_length = kwargs.pop('max_length', None)
        super().__init__(**kwargs)
        
                
    def run_validation(self, data=serializers.empty):
        if data == '':
            if not self.allow_blank:
                self.fail('blank')
            return {
                 'value': ''
            }
        else:
            if data and self.max_length and len(str(data)) > self.max_length:
                self.fail('too_long')
        return super().run_validation(str(data))
    
    def to_internal_value(self, data):

        value = {
            'value': str(data)
        }
        return value


    def to_representation(self, obj):
        """ 
        In certain cases i want to be able to load the id, in others i don't, i want to retrieve only the string.
        this is why i use load_ids parameter for. For form type of field i check if the form_value.field_type is equal
        the field.type with this if the user change from a form field.type to a text field.type, then i retrieve the hole text
        to the user and not the id the field references to.
        """
        from reflow_server.data.services import RepresentationService

        if obj and obj.value != '':
            # what is this for? this is for loading empty value instead of the respresented value
            # we usually do this when the field_type is 'form' or 'user', so it is data that the user
            # probably wont understand what it is. 'form' and 'user' field_types actually hold the id
            # of the reference, if the user change the type of the field and open the formulary he then
            # needs to see empty values
            #is_to_load_empty_value_instead_of_represented = not self.use_state and obj.field_type.type in ['form', 'user'] and obj.field_type != obj.field.type
            
            if self.load_ids and obj.field_type.type == 'form' and obj.field.type.type != 'form':
                self.load_ids = False
            if not self.use_state:
                date_configuration_date_format_type = obj.field.date_configuration_date_format_type
                number_configuration_number_format_type = obj.field.number_configuration_number_format_type
                form_field_as_option = obj.field.form_field_as_option
            else: 
                date_configuration_date_format_type = obj.date_configuration_date_format_type
                number_configuration_number_format_type = obj.number_configuration_number_format_type
                form_field_as_option = obj.form_field_as_option

            representation = RepresentationService(
                obj.field_type.type, 
                date_configuration_date_format_type, 
                number_configuration_number_format_type, 
                form_field_as_option, 
                self.load_ids
            )
            return representation.representation(obj.value)
        else:
            return ''