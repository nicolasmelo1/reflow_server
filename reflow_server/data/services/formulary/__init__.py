from reflow_server.formulary.managers import default_field_value
from django.db import transaction

from reflow_server.core.events import Event
from reflow_server.authentication.models import UserExtended
from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.formulary.models import DefaultFieldValue, Form, Field, PublicAccessField
from reflow_server.data.models import FormValue, DynamicForm
from reflow_server.data.services.formulary.data import FormularyData
from reflow_server.data.services.formulary.pre_save import PreSave
from reflow_server.data.services.formulary.post_save import PostSave


class FormularyDataService(PreSave, PostSave):
    def __init__(self, user_id, company_id, form_name, public_access_key=None):
        """
        This object handles the save and update of the data of a single form.

        Since when saving we have to guarantee many operations, with this service we
        can control more easily.

        To use this class correctly, read `.add_formulary_data()` first so you can have a better
        understading on how to use it.
        """
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name
        self.public_access_key = public_access_key
        self.post_save_process = list()
    # ------------------------------------------------------------------------------------------
    def add_formulary_data(self, form_data_uuid, form_data_id=None, duplicate=False):
        """
        This function is meant to be run inside a loop of insertion. it's important to 
        understand that this is required for running any other method inside of this service.
        It saves the data of the formulary as objects so we can work with it without needding
        to know anything outside of this class.

        Okay, but how does it work: as you remember formularies are a conjunction of sections, and
        inside each sections there are the fields. That's exactly what we mimic here.

        When you run this function we return to you a FormularyData object that exposes
        `.add_section_data()` method for you to add your sections. This object will contain an array
        with all of your sections, but to add those you need to add each section using
        the `.add_section_data()` method. The `.add_section_data()` method will return to you a 
        SectionData object which exposes the `.add_field_value()` method to insert each field inside 
        of the section. This way we can have a complete formulary being built as objects and work 
        with it instead of working directly with serializers.

        Args:
            form_data_uuid: The uuid of the formulary
            form_data_id (int, optional): The id of the formulary, this is usually set if you are editing an
                                          instance, otherwise you can leave it as null (default as None)
            duplicate_form_data_id (int, optional): If you are trying to duplicate a formulary set it to True 
                                                    and make sure `form_data_id` is defined (default as False).
        Returns:
            FormularyData: The object for you which you can insert sections and field_vales
        """
        if duplicate:
            self.duplicate_form_data_id = form_data_id
            form_data_id = None
        
        self.formulary_data = FormularyData(form_data_uuid, form_data_id)
        return self.formulary_data
    # ------------------------------------------------------------------------------------------
    def __send_events_post_save(self, formulary_instance_id): 
        """
        Sends all of the events it has to send for the users of the company AFTER the formulary has been saved.

        Args:
            formulary_instance_id (id): The id of the updated or created DynamicForm instance
        """
        # register the event that the formulary was updated or created
        formulary_data_was_created = self.formulary_data.form_data_id == None
        is_public = self.public_access_key != None
        if formulary_data_was_created:
            Event.register_event('formulary_data_created', {
                'user_id': self.user_id,
                'company_id': self.company_id,
                'form_id': self.form.id,
                'is_public': is_public,
                'form_data_id': formulary_instance_id
            })
        else:
            Event.register_event('formulary_data_updated', {
                'user_id': self.user_id,
                'company_id': self.company_id,
                'form_id': self.form.id,
                'is_public': is_public,
                'form_data_id': formulary_instance_id
            })
        # updates the pre_notifications
        PreNotificationService.update(self.company_id)
    # ------------------------------------------------------------------------------------------
    @property
    def __default_field_values_to_use_in_formulary(self):
        """
        Creates a dict of default field value instances by each field_id. With this we can then force the default value if
        is not defined.

        Raises:
            AssertionError: Both `.__sections_to_use_in_formulary()` and `.__fields_to_use_in_formulary()` should be called
            before this function

        Returns:
            dict: A dict where each key is a field_id, and the value of each key is a list of DefaultFieldValue instances
            Example:
            {
                1: [reflow_server.formulary.models.DefaultFieldValue],
                2: [reflow_server.formulary.models.DefaultFieldValue, reflow_server.formulary.models.DefaultFieldValue]
            }
        """
        if hasattr(self, 'sections') and hasattr(self, 'fields'):
            default_field_value_by_field_id = {}
            default_field_values = DefaultFieldValue.data_.default_field_values_by_field_ids(self.fields.values_list('id', flat=True))
            for default_field_value in default_field_values:
                if default_field_value_by_field_id.get(default_field_value.field_id, None):
                    default_field_value_by_field_id[default_field_value.field_id] = default_field_value_by_field_id[default_field_value.field_id] + [default_field_value]
                else:
                    default_field_value_by_field_id[default_field_value.field_id] = [default_field_value]
            return default_field_value_by_field_id
        else:
            raise AssertionError('You should call `.__sections_to_use_in_formulary()` and `.__fields_to_use_in_formulary()` before calling the `.__default_field_values_to_use_in_formulary()` property') 
    # ------------------------------------------------------------------------------------------
    @property
    def __fields_to_use_in_formulary(self):
        """
        Retrieves the fields we should use when validating the formulary, if it's a public access, we use only the fields that the original user
        set to public.

        Raises:
            AssertionError: The sections to use should be retrieved first than the fields. We use those sections to filter the fields we should use

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Field): A queryset of Field instances to use when saving the data.
        """
        if hasattr(self, 'sections'):
            fields = Field.data_.fields_enabled_ordered_by_form_and_order_by_main_form_name_and_sections(self.form_name, self.sections)
            if self.public_access_key:
                field_ids = PublicAccessField.data_.field_ids_by_public_access_key(self.public_access_key)
                fields = fields.filter(id__in=field_ids)
            return fields
        else:
            raise AssertionError('You should call `.__sections_to_use_in_formulary()` property before calling this `.__fields_to_use_in_formulary()` property')
    # ------------------------------------------------------------------------------------------
    @property
    def __sections_to_use_in_formulary(self):
        """
        Retrieves the sections to use to validate the formulary data on. We validate the conditionals and everything else based on the sections retrieves here.
        We need this in a separate function because of public access. When an unauthenticated user tries to save a data we need to validate the data based on the 
        sections the user set a public access.

        Returns:
            django.db.models.QuerySet(reflow_server.formulary.models.Form): A queryset of Form instance to use to validate the data on.
            Those Form instances have `depends_on` as NOT NULL.
        """
        sections = Form.data_.sections_enabled_by_main_form_name_and_company_id(self.form_name, self.company_id)
        if self.public_access_key:
            sections_ids = PublicAccessField.data_.section_ids_by_public_access_key(self.public_access_key)
            sections = sections.filter(id__in=sections_ids)
        return sections
    # ------------------------------------------------------------------------------------------
    @property
    def __check_formulary_data(self):
        if not hasattr(self, 'formulary_data'):
            raise AssertionError('You should call `.add_formulary_data()` method before calling '
                                 'the method you are trying to call')
    # ------------------------------------------------------------------------------------------
    def is_valid(self):
        """
        Cleans the data (the internal data, not outside, we don't clean the data on your serializer or whatever directly)
        and validates the formulary data.

        If your data is not valid you can call `.errors` to retrieve your error.
        """
        self.__check_formulary_data

        # define everything we are gonna use while validating and saving the data
        self.user = UserExtended.data_.user_by_user_id(self.user_id)
        self.form = Form.objects.filter(
            form_name=self.form_name, 
            group__company_id=self.company_id
        ).first()
        self.sections = self.__sections_to_use_in_formulary
        self.fields = self.__fields_to_use_in_formulary
        self.default_field_value_by_field_id = self.__default_field_values_to_use_in_formulary 
        self.formulary_data = self.clean_data(self.formulary_data)

        self.validated = True
        return self.formulary_data_is_valid(self.formulary_data)        
    # ------------------------------------------------------------------------------------------
    @transaction.atomic
    def save(self):
        """
        This method should be called after calling `.add_formulary_data()` and `.is_valid()`. This
        method effectively saves the data present on FormularyData. While it saves the data from each field
        it sends the saved instance to .add_saved_field_value_to_post_process(), to post process after the 
        data has been saved. Since we add the saved_instance to post_process, after finishing saving the hole 
        formulary data we call .post_save() to post process the instances (it's when we save the files to s3, when we
        calculate formulas and when we create ids for `id` field_type).
        After that the formulary is basically saved, then we call PreNotificationService to update the pre_notifications
        of the company with the new data. And then we return the instance of the created or updated FORMULARY (not 
        Sections or FormValue).
        
        Raises:
            AssertionError: You should call `.is_valid()` method before trying to save the data.' 

        Returns:
            reflow_server.data.models.DynamicForm: The formulary instance, we don't retrieve sections nor values
        """
        self.__check_formulary_data

        if not hasattr(self, 'validated'):
            raise AssertionError('You should call `.is_valid()` method before trying to save the data.')
        
        formulary_instance = DynamicForm.data_.create_or_update_main_form_instance(
            self.form.id,
            self.formulary_data.uuid,
            self.user_id,
            self.company_id,
            main_form_instance_id=self.formulary_data.form_data_id
        )

        for section in self.formulary_data.get_sections:
            section_instance = DynamicForm.data_.create_or_update_section_instance(
                section.section_id,
                section.section_uuid,
                self.user_id,
                self.company_id,
                main_form_instance=formulary_instance,
                section_instance_id=section.section_data_id
            )
    
            # updates the section data with the newly section instance id so when deleting we consider this new value (used for conditionals)
            section.section_data_id = section_instance.id

            for field_value in section.get_field_values:
                field = self.fields.filter(name=field_value.field_name).first()
                form_value_instance = FormValue.data_.create_or_update(
                    form_value_id=field_value.field_value_data_id,
                    field=field,
                    field_type=field.type,
                    company_id=self.company_id,
                    date_configuration_date_format_type=field.date_configuration_date_format_type,
                    period_configuration_period_interval_type=field.period_configuration_period_interval_type,
                    number_configuration_number_format_type=field.number_configuration_number_format_type,
                    formula_configuration=field.formula_configuration,
                    form_field_as_option=field.form_field_as_option if field.type.type == 'form' else None,
                    value=field_value.value,
                    section=section_instance
                )
                # updates the field_value data with the newly field_value instance id so when deleting
                # removed data can consider this new value (so we don't delete it)
                field_value.update_field_value_data_id(form_value_instance.id)

                self.add_saved_field_value_to_post_process(section_instance, form_value_instance)

        self.post_save(self.formulary_data) 

        # sends events to the users subscribed
        self.__send_events_post_save(formulary_instance.id)

        return formulary_instance
    # ------------------------------------------------------------------------------------------
