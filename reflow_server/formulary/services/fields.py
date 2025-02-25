from django.db import transaction

from reflow_server.core.events import Event
from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.data.services.representation import RepresentationService
from reflow_server.data.models import FormValue
from reflow_server.draft.services import DraftService
from reflow_server.draft.models import Draft
from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.services.options import FieldOptionsService
from reflow_server.formulary.services.utils import Settings
from reflow_server.formulary.services.default_attachment import DefaultAttachmentService
from reflow_server.formulary.models import Form, Field, FieldOptions, PublicAccessField, DefaultFieldValue, \
    FieldType, UserAccessedBy, FormulaVariable

import uuid


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
                    field_instance.date_configuration_date_format_type_id, 
                    field_instance.number_configuration_number_format_type_id,
                    field_instance.form_field_as_option_id
                )

                DefaultFieldValue.formulary_.update_or_create(
                    field_instance.id, 
                    representation.to_internal_value(default_field_value.value), 
                    default_field_value.default_value_id
                )
    # ------------------------------------------------------------------------------------------
    def save_formula_variables(self, field_instance, field_formula_variables):
        """
        Saves the all of the formula variables of a formula field

        Args:
            field_instance (reflow_server.formulary.models.Field): The Field instance id that was created or updated
            field_formula_variables (list(reflow_server.formulary.services.data.FormulaVariableData)): A list of FormulaVariableData objects
        """
        saved_uuids = []
        for order, field_formula_variable in enumerate(field_formula_variables):
            saved_uuids.append(field_formula_variable.uuid)
            FormulaVariable.formulary_.save_formula_variable(
                field_id=field_instance.id, 
                variable_id=field_formula_variable.variable_id, 
                uuid=field_formula_variable.uuid,
                order=order
            )

        FormulaVariable.formulary_.delete_formula_variables_not_in_variable_ids_by_uuids(field_instance.id, saved_uuids)
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
    def __create_user_accessed_by_when_field_is_created(self, field_id):
        """
        When the field is of 'user' type, we need to create the options the user can access, in other words, all of the users.
        So this function is to give the user full access for all users in this option.

        Args:
            field_id (int): The newly created Field instance id
        """
        users_from_company = UserExtended.formulary_.users_active_by_company_id(self.company_id)
        for user in users_from_company:
            for user_option in users_from_company:
                UserAccessedBy.formulary_.create_or_update(
                    user_id=user.id,
                    field_id=field_id,
                    user_option_id=user_option.id
                )
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
                   field_type, field_options_data=None, default_field_value_data=None, 
                   field_formula_variables=None, field_uuid=None, is_long_text_a_rich_text=False, 
                   instance=None, is_adding_theme=False):
        
        is_new_field = False
        if instance == None or instance.id == None:
            is_new_field = True
            instance = Field()
        if field_uuid == None:
            field_uuid = uuid.uuid4()

        field_options_service = FieldOptionsService(self.company_id)

        existing_fields = Field.objects.filter(
            form=section, 
            form__depends_on__group__company_id=self.company_id, 
            form__depends_on_id=self.form.id
        ).exclude(
            id=instance.id if instance else None
        ).order_by('form__order', 'order')
        
        self.update_order(existing_fields, order, instance.id if instance else None)          

        instance.enabled = enabled
        instance.uuid = field_uuid
        instance.label_name = label_name
        instance.order = order
        instance.is_unique = is_unique
        instance.field_is_hidden = field_is_hidden
        instance.label_is_hidden = label_is_hidden
        instance.placeholder = placeholder
        instance.required = required
        instance.is_long_text_rich_text = is_long_text_a_rich_text
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

        if field_formula_variables != None:
            self.save_formula_variables(instance, field_formula_variables)

        if instance.type.type in ['option', 'multi_option']:
            field_options_service.create_new_field_options(instance, field_options_data)

        # We don't access directly the id of the field option, only the values, we use this to delete or add a field Option
        elif FieldOptions.objects.filter(field=instance).exists():
            field_options_service.remove_field_options_from_field(instance.id)
        if is_new_field and instance.type.type == 'user':
            self.__create_user_accessed_by_when_field_is_created(instance.id)

        events_data = {
            'user_id': self.user_id,
            'company_id': self.company_id,
            'form_id': self.form.id,
            'section_id': instance.form_id,
            'field_id': instance.id
        }
        if is_adding_theme == False:
            if is_new_field:
                Event.register_event('field_created', events_data)
            else:
                Event.register_event('field_updated', events_data)

        return instance
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def is_form_field_type_not_valid(field_type_id, form_field_as_option_field_id):
        field_type = FieldType.objects.filter(id=field_type_id).first()
        return field_type and field_type.type == 'form' and not form_field_as_option_field_id
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def is_option_field_type_not_valid(field_type_id, field_options_length):
        field_type = FieldType.objects.filter(id=field_type_id).first()
        return field_type and field_type.type in ['option', 'multi_option'] and field_options_length == 0
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def is_label_name_not_unique(field_id, company_id, section_id, label_name):
        """
        Checks is the label name already exists in the formulary. Every formulary can have one and just one
        field name, it is not possible to have 2 equal field names on the same formulary.

        Args:
            field_id (int): A Field instance id, we use this to exclude the actual field_id that is being updated
                            Imagine we are updating the field 'Status' which already exists, this field should be 
                            excluded to evaluate if the name exists.
            company_id (int): A Company instance id, don't have much to say, it just enables a better filtering of the data.
            section_id (int): A Form instance id with depends_on as NOT NULL. we use this to retrieve the MAIN Form instance id.
            label_name (str): And last but not least the label_name of the field, the new label_name or the updated label name,
                              we compare it with all of the other fields of the formulary.

        Returns:
            bool: Returns True if the label_name IS NOT unique and False if it is unique. False is good, True is bad.
        """
        section = Form.objects.filter(id=section_id, depends_on__group__company_id=company_id).first()
        if section:
            main_form_id = section.depends_on_id
            return Field.formulary_.field_by_label_name_company_id_and_main_form_id_excluding_id_exists(
                field_id=field_id,
                label_name=label_name,
                company_id=company_id,
                main_form_id=main_form_id
            )
        else:
            return False
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def retrieve_actual_field_type_for_field(field_id, field_type):
        if field_type.is_dynamic_evaluated:
            latest_form_value = FormValue.formulary_.latest_form_value_field_type_by_field_id(field_id)
            if latest_form_value:
                return latest_form_value.field_type
    
        return field_type
