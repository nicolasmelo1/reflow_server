from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.services.utils import Settings
from reflow_server.formulary.models import Form, Field, FieldOptions, OptionAccessedBy


class FieldService(Settings):
    def __init__(self, user_id, company_id, form_id):
        self.user_id = user_id
        self.company_id = company_id
        self.form_id = form_id

    def save_field(self, instance, enabled, label_name, order, is_unique, field_is_hidden, 
                   label_is_hidden, placeholder, required, section, form_field_as_option, 
                   formula_configuration, date_configuration_auto_create, date_configuration_auto_update,
                   number_configuration_number_format_type, date_configuration_date_format_type,
                   period_configuration_period_interval_type, field_type, field_options=list()):
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
            created_field_options=list()
            FieldOptions.objects.exclude(option__in=field_options).filter(field=instance).delete()
            for field_option_index, field_option in enumerate(field_options):
                option, created = FieldOptions.objects.update_or_create(option=field_option,
                                                                        field=instance,
                                                                        defaults={
                                                                            'order': field_option_index
                                                                        })
                
                if created:
                    created_field_options.append(option)
            
            # when you create a new field option, all of the users have access to this option
            # automatically
            company_user_ids = UserExtended.objects.filter(company_id=self.company_id, is_active=True).values_list('id', flat=True)

            OptionAccessedBy.objects.bulk_create([
                OptionAccessedBy(field_option=created_field_option, user_id=company_user_id)
                for created_field_option in created_field_options for company_user_id in company_user_ids
            ])

        # We don't access directly the id of the field option, only the values, we use this to delete or add a field Option
        elif FieldOptions.objects.filter(field=instance).exists():
            FieldOptions.objects.filter(field=instance).delete()

        return instance