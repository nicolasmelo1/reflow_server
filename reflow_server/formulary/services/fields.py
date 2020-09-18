from django.db import transaction

from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.services.options import FieldOptionsService
from reflow_server.formulary.services.utils import Settings
from reflow_server.formulary.models import Form, Field, FieldOptions, OptionAccessedBy


class FieldService(Settings):
    def __init__(self, user_id, company_id, form_id):
        self.user_id = user_id
        self.company_id = company_id
        self.form_id = form_id
    
    @transaction.atomic
    def save_field(self, enabled, label_name, order, is_unique, field_is_hidden, 
                   label_is_hidden, placeholder, required, section, form_field_as_option, 
                   formula_configuration, date_configuration_auto_create, date_configuration_auto_update,
                   number_configuration_number_format_type, date_configuration_date_format_type,
                   period_configuration_period_interval_type, field_type, field_options=list(), instance=None):
        if instance == None:
            instance = Field()
                   
        field_options_service = FieldOptionsService(self.user_id, self.company_id)


        existing_fields = Field.objects.filter(
            form=section, 
            form__depends_on__group__company_id=self.company_id, 
            form__depends_on_id=self.form_id
        ).exclude(
            id=instance.id if instance else None
        ).order_by('form__order', 'order')
        
        self.update_order(existing_fields, order)          


        instance.enabled = enabled
        instance.label_name = label_name
        instance.order = order
        instance.is_unique = is_unique
        instance.field_is_hidden = field_is_hidden
        instance.label_is_hidden = label_is_hidden
        instance.placeholder = placeholder
        instance.required = required
        instance.form_id = section.id if isinstance(section, Form) else section
        instance.form_field_as_option = form_field_as_option
        instance.formula_configuration = formula_configuration
        instance.date_configuration_auto_create = date_configuration_auto_create
        instance.date_configuration_auto_update = date_configuration_auto_update
        instance.number_configuration_number_format_type = number_configuration_number_format_type
        instance.date_configuration_date_format_type = date_configuration_date_format_type
        instance.period_configuration_period_interval_type = period_configuration_period_interval_type
        instance.type = field_type
        instance.name = self.format_name('field', instance.id, instance.name, label_name)
        instance.save()
        

        # updates the pre_notifications
        PreNotificationService.update(self.company_id)
        
        if instance.type.type in ['option', 'multi_option']:
            field_options_service.create_new_field_options(instance, field_options)

        # We don't access directly the id of the field option, only the values, we use this to delete or add a field Option
        elif FieldOptions.objects.filter(field=instance).exists():
            field_options_service.remove_field_options_from_field(instance.id)

        return instance