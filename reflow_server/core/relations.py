from rest_framework import serializers

from django.utils.translation import gettext_lazy as _

field_types_cache = {}

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
        
    def initialize_field_types_cache(self): 
        from reflow_server.formulary.models import FieldType

        if not field_types_cache:
            field_types = FieldType.objects.all()
            for field_type in field_types:
                field_types_cache[field_type.id] = field_type.type

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
        from reflow_server.data.models import FormValue

        form_value = FormValue.objects.filter(id=obj.id).values(
            'value', 
            'form_field_as_option_id', 
            'number_configuration_number_format_type_id',
            'date_configuration_date_format_type_id',
            'field_type_id', 
            'field__type_id'
        ).first()
        
        self.initialize_field_types_cache()
        
        if form_value and form_value['value'] != '':
            is_form_value_of_form_type = field_types_cache[form_value['field_type_id']] == 'form'
            is_field_of_form_type = field_types_cache[form_value['field__type_id']] != 'form'

            if self.load_ids and is_form_value_of_form_type and is_field_of_form_type:
                self.load_ids = False

            representation = RepresentationService(
                field_types_cache[form_value['field_type_id']], 
                form_value['date_configuration_date_format_type_id'], 
                form_value['number_configuration_number_format_type_id'], 
                form_value['form_field_as_option_id'], 
                self.load_ids
            )
                
            represented_value = representation.representation(form_value['value'])

            return represented_value
        else:
            return ''
