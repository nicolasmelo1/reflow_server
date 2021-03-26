from django.conf import settings
from django.db import transaction


from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.draft.services import DraftService
from reflow_server.draft.models import Draft
from reflow_server.formulary.services.options import FieldOptionsService
from reflow_server.formulary.services.utils import Settings
from reflow_server.formulary.models import Form, Field, FieldOptions, PublicAccessField, DefaultFieldValue, DefaultFieldValueAttachments


class FieldService(Settings):
    def __init__(self, user_id, company_id, form_id):
        self.user_id = user_id
        self.company_id = company_id
        self.form = Form.objects.filter(id=form_id).first()
    # ------------------------------------------------------------------------------------------
    def save_default_values(self, field_instance, field_type, default_field_values_data):
        for default_field_value in default_field_values_data:
            if field_type.type == 'attachment':
                draft_id = DraftService.draft_id_from_draft_string_id(default_field_value.value)
                if draft_id != -1:
                    draft_instance = Draft.formulary_.draft_by_draft_id_user_id_and_company_id(draft_id, self.user_id, self.company_id)
                    real_file_name = draft_instance.value

                    default_field_value_instance = DefaultFieldValue.formulary_.update_or_create(
                        field_instance.id, real_file_name, default_field_value.default_value_id
                    )

                    bucket_key = "{file_default_attachments_path}/{default_field_value_instance_id}/".format(
                        file_default_attachments_path=settings.S3_FILE_DEFAULT_ATTACHMENTS_PATH,
                        default_field_value_instance_id=default_field_value_instance.id
                    )

                    file_size = draft_instance.file_size
                    file_url = DraftService(self.company_id, self.user_id)\
                        .copy_file_from_draft_string_id_to_bucket_key(
                            default_field_value.value,
                            bucket_key
                        )

                    default_field_value_attachment_instance = DefaultFieldValueAttachments.formulary_.update_or_create(
                        file_name=real_file_name,
                        file_url=file_url,
                        file_size=file_size
                    )
                    
                    default_field_value_instance.default_attachment = default_field_value_attachment_instance
                    default_field_value_instance.save()
            else:
                DefaultFieldValue.formulary_.update_or_create(
                    field_instance.id, 
                    default_field_value.value, 
                    default_field_value.default_value_id
                )
    # ------------------------------------------------------------------------------------------
    def get_public_fields_from_section(self, public_access_key, section_id):
        """
        Retrieve all of the fields that are public and accessible by unauthenticated users

        Args:
            public_access_key (str): [description]
            section_id (int): A Form instance id with depends_on as NOT NULL
        """
        field_ids = PublicAccessField.formulary_.field_ids_by_public_access_key(public_access_key)
        return Field.objects.filter(id__in=field_ids, form_id=section_id, form__depends_on=self.form, form__depends_on__group__company_id=self.company_id)
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def save_field(self, enabled, label_name, order, is_unique, field_is_hidden, 
                   label_is_hidden, placeholder, required, section, form_field_as_option, 
                   formula_configuration, default_field_value_data, date_configuration_auto_create, 
                   date_configuration_auto_update, number_configuration_number_format_type, 
                   date_configuration_date_format_type, period_configuration_period_interval_type, 
                   field_type, field_options_data=None, instance=None):
        if instance == None:
            instance = Field()
                   
        field_options_service = FieldOptionsService(self.company_id)

        existing_fields = Field.objects.filter(
            form=section, 
            form__depends_on__group__company_id=self.company_id, 
            form__depends_on_id=self.form.id
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
        if field_type.type == 'date':
            PreNotificationService.update(self.company_id)
        
        self.save_default_values(instance, field_type, default_field_value_data)

        if instance.type.type in ['option', 'multi_option']:
            field_options_service.create_new_field_options(instance, field_options_data)

        # We don't access directly the id of the field option, only the values, we use this to delete or add a field Option
        elif FieldOptions.objects.filter(field=instance).exists():
            field_options_service.remove_field_options_from_field(instance.id)

        from reflow_server.formulary.events import FormularyEvents        
        FormularyEvents.send_updated_formulary(self.company_id, self.form.id, self.form.form_name)

        return instance