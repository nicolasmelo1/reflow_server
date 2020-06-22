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
            if self.load_ids and obj.field_type.type == 'form' and obj.field.type.type != 'form':
                self.load_ids = False

            representation = RepresentationService(
                obj.field_type.type, 
                obj.date_configuration_date_format_type.id if obj.date_configuration_date_format_type else None, 
                obj.number_configuration_number_format_type.id if obj.number_configuration_number_format_type else None, 
                obj.form_field_as_option.id if obj.form_field_as_option else None, 
                self.load_ids
            )
            return representation.representation(obj.value)
        else:
            return ''