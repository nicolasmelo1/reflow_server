from reflow_server.formulary.services.utils import Settings
from reflow_server.formulary.models import Field


class FieldService(Settings):
    def __init__(self, user_id, form_id, company_id):
        self.user_id = user_id
        self.company_id = company_id
        self.form_id = form_id

    def save_field(self, instance, enabled, label_name, order, is_unique, field_is_hidden, 
                   label_is_hidden, placeholder, required, section, form_field_as_option, 
                   formula_configuration, date_configuration_auto_create, date_configuration_auto_update,
                   number_configuration_number_format_type, date_configuration_date_format_type,
                   period_configuration_period_interval_type, field_type):
        pass
        """"
        instance.enabled = validated_data['enabled']
        instance.label_name = validated_data['label_name']
        instance.order = validated_data['order']
        instance.is_unique = validated_data['is_unique']
        instance.field_is_hidden = validated_data['field_is_hidden']
        instance.label_is_hidden = validated_data['label_is_hidden']
        instance.placeholder = validated_data.get('placeholder', None)
        instance.required = validated_data['required']
        instance.form = validated_data['form']
        instance.form_field_as_option = Field.objects.filter(
            id=validated_data['form_field_as_option']['id']
            if 'form_field_as_option' in validated_data and validated_data['form_field_as_option'] else '',
            form__depends_on_id=validated_data['form_field_as_option']['form']['depends_on_id']
            if 'form_field_as_option' in validated_data and validated_data['form_field_as_option'] else '',
            form__company_id=self.context['company']
        ).first() if validated_data['form_field_as_option'] else None
        instance.formula_configuration = validated_data['formula_configuration'] if validated_data['formula_configuration'] != '' else None
        instance.date_configuration_auto_create = validated_data['date_configuration_auto_create']
        instance.date_configuration_auto_update = validated_data['date_configuration_auto_update']
        instance.number_configuration_number_format_type = validated_data.get('number_configuration_number_format_type', None)
        instance.date_configuration_date_format_type = validated_data.get('date_configuration_date_format_type', None)
        instance.period_configuration_period_interval_type = validated_data.get('period_configuration_period_interval_type', None)
        instance.type = validated_data['type']
        instance.name = self.new_field_name
        instance.save()

        NotificationHelper.change_notification_field_names(validated_data['name'], self.new_field_name, self.context['company'])

        users = UserExtended.objects.filter(company_id=self.context['company'], is_active=True).values_list('id', flat=True)
        if instance.type.type in ['option', 'multi_option']:
            FieldOptions.objects.exclude(
                option__in=[list_field_option['option'] for list_field_option in validated_data['field_option']])\
                .filter(field=instance).delete()
            for field_option_index, field_option in enumerate(validated_data['field_option']):
                option, created = FieldOptions.objects.update_or_create(option=field_option['option'],
                                                                        field=instance,
                                                                        defaults={
                                                                            'order': field_option_index
                                                                        })
                # this is a business rule, when you create a new field option, all of the users have access to this option
                # automatically
                if created:
                    OptionAccessedBy.objects.bulk_create([
                        OptionAccessedBy(field_option=option, user_id=user)
                        for user in users
                    ])

        # We don't access directly the id of the field option, only the values, we use this to delete or add a field Option
        elif FieldOptions.objects.filter(field=instance).exists():
            FieldOptions.objects.filter(field=instance).delete()
        """