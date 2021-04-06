from django.conf import settings
from django.db import transaction


from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.data.services.representation import RepresentationService
from reflow_server.draft.services import DraftService
from reflow_server.draft.models import Draft
from reflow_server.formulary.services.options import FieldOptionsService
from reflow_server.formulary.services.utils import Settings
from reflow_server.formulary.services.default_attachment import DefaultAttachmentService
from reflow_server.formulary.models import Form, Field, FieldOptions, PublicAccessField, DefaultFieldValue, DefaultFieldValueAttachments


class FieldService(Settings):
    def __init__(self, user_id, company_id, form_id):
        self.user_id = user_id
        self.company_id = company_id
        self.form = Form.objects.filter(id=form_id).first()
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def save_default_values(self, field_instance, default_field_values_data):
        """
        Saves the default values, default values are values that are used when no value is provided for a particular field.
        So when the user saves a new formulary data this is automatically set.

        Args:
            field_instance (reflow_server.formulary.models.Field): The field instance that was created or updated 
            default_field_values_data (list(reflow_server.formulary.services.data.DefaultFieldData)): List of DefaultFieldData objects
            that is used to save the field data.
        """
        # first removes what was deleted, then adds the new defaults.
        self.remove_default_values(field_instance, default_field_values_data)

        for default_field_value in default_field_values_data:
            if field_instance.type.type == 'attachment':
                draft_id = DraftService.draft_id_from_draft_string_id(default_field_value.value)
                if draft_id != -1:
                    draft_instance = Draft.formulary_.draft_by_draft_id_user_id_and_company_id(draft_id, self.user_id, self.company_id)
                    if draft_instance:
                        real_file_name = draft_instance.value
                        file_size = draft_instance.file_size

                        default_field_value_instance = DefaultFieldValue.formulary_.update_or_create(
                            field_instance.id, real_file_name, default_field_value.default_value_id
                        )
                        default_field_value_attachment_instance = DefaultAttachmentService(self.company_id, self.user_id, field_instance.id).save_from_draft_string_id(
                            default_field_value.value, 
                            default_field_value_instance.id, 
                            real_file_name,
                            file_size
                        )
                        
                        default_field_value_instance.default_attachment = default_field_value_attachment_instance
                        default_field_value_instance.save()
            else:
                representation = RepresentationService(
                    field_instance.type.type, 
                    field_instance.date_configuration_date_format_type, 
                    field_instance.number_configuration_number_format_type,
                    field_instance.form_field_as_option
                )

                DefaultFieldValue.formulary_.update_or_create(
                    field_instance.id, 
                    representation.to_internal_value(default_field_value.value), 
                    default_field_value.default_value_id
                )
    # ------------------------------------------------------------------------------------------
    def remove_default_values(self, field_instance, default_field_values_data):
        """
        Removes all of the default values when they are removed, we need to remove them Before saving the new ones, when saving the new ones we 
        still will not have the DefaultFieldValue id, so we need to remove before.

        Args:
            field_instance (reflow_server.models.formulary.Field): The saved or updated Field instance
            default_field_values_data (list(reflow_server.formulary.services.data.DefaultFieldData)): List of DefaultFieldData objects
            that is used to save the field data.
            """
        default_field_value_ids_to_consider = [default_field_value.default_value_id for default_field_value in default_field_values_data]

        if field_instance.type.type == 'attachment':
            DefaultAttachmentService(self.company_id, self.user_id, field_instance.id).remove_default_attachment(default_field_value_ids_to_consider)
        
        DefaultFieldValue.formulary_.delete_default_field_values_by_field_id_excluding_default_field_value_ids(
            field_instance.id, 
            default_field_value_ids_to_consider
        )
    # ------------------------------------------------------------------------------------------ 
    def remove_field(self, field_id):
        """
        Removes a field by it's id.

        Args:
            field_id (int): A Field instance id.
        """
        instance = Field.objects.filter(
            id=field_id, 
            form__depends_on__group__company_id=self.company_id, 
            form__depends_on_id=self.form.id
        ).first()
        if instance:
            # needs to remove the defaults manually and before deleting because of the attachments.
            self.remove_default_values(instance, [])
            instance.delete()
    # ------------------------------------------------------------------------------------------ 
    @transaction.atomic
    def get_public_fields_from_section(self, public_access_key, section_id):
        """
        Retrieve all of the fields that are public and accessible by unauthenticated users

        Args:
            public_access_key (str): The public access key defined in the PublicAccess instance
            section_id (int): A Form instance id with depends_on as NOT NULL
        """
        field_ids = PublicAccessField.formulary_.field_ids_by_public_access_key(public_access_key)
        return Field.objects.filter(id__in=field_ids, form_id=section_id, form__depends_on=self.form, form__depends_on__group__company_id=self.company_id)
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def save_field(self, enabled, label_name, order, is_unique, field_is_hidden, 
                   label_is_hidden, placeholder, required, section, form_field_as_option, 
                   formula_configuration, date_configuration_auto_create, 
                   date_configuration_auto_update, number_configuration_number_format_type, 
                   date_configuration_date_format_type, period_configuration_period_interval_type, 
                   field_type, field_options_data=None, default_field_value_data=None, instance=None):
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
            
        if default_field_value_data != None:
            self.save_default_values(instance, default_field_value_data)

        if instance.type.type in ['option', 'multi_option']:
            field_options_service.create_new_field_options(instance, field_options_data)

        # We don't access directly the id of the field option, only the values, we use this to delete or add a field Option
        elif FieldOptions.objects.filter(field=instance).exists():
            field_options_service.remove_field_options_from_field(instance.id)

        from reflow_server.formulary.events import FormularyEvents        
        FormularyEvents.send_updated_formulary(self.company_id, self.form.id, self.form.form_name)

        return instance