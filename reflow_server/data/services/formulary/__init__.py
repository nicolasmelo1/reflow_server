from django.db import transaction

from reflow_server.authentication.models import UserExtended
from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.formulary.models import Form, Field
from reflow_server.data.models import FormValue, DynamicForm
from reflow_server.data.services.formulary.data import FormularyData
from reflow_server.data.services.formulary.pre_save import PreSave
from reflow_server.data.services.formulary.post_save import PostSave


class FormularyService(PreSave, PostSave):
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name
        self.post_save_process = list()

    def add_formulary_data(self, form_data_id=None, duplicate=False):
        """
        This function is meant to be run inside a loop of insertion. it's important to 
        understand that this is required for running any other method inside of this service.
        It saves the data of the formulary as objects so we can work with it without needding
        to know anything outside of this serializer.

        Okay, but how does it work: as you remember formularies are a conjunction of sections, and
        inside each sections there are the fields. That's exactly what we mimic here.

        When you run this function we return to you a FormularyData object that exposes
        `.add_section_data()` method, for you to add your sections. After you add your section using
        the `.add_section_data()` method we return to you a SectionData object which exposes the
        `.add_field_value()` method to insert each field inside of the section. This way we can have
        a complete formulary being built as objects and work with it instead of working with serializers,
        dicts or other non pythonic objects.

        Args:
            form_data_id (int, optional): The id of the formulary, this is usually set if you are editing an
                                          instance, otherwise you can leave it as null (default as None)
            duplicate_form_data_id (int, optional): If you are trying to duplicate a formulary set it to True 
                                                    make sure and make sure `form_data_id` is defined (default as False).
        Returns:
            FormularyData: The object for you which you can insert sections and field_vales
        """
        if duplicate:
            self.duplicate_form_data_id = form_data_id
            form_data_id = None
        self.formulary_data = FormularyData(form_data_id)
        return self.formulary_data

    @property
    def __check_formulary_data(self):
        if not hasattr(self, 'formulary_data'):
            raise AssertionError('You should call `.add_formulary_data()` method before calling '
                                 'the method you are trying to call')

    def is_valid(self):
        """
        Cleans the data (the internal data, not outside, we don't clean the data on your serializer or whatever directly)
        and validates the formulary data.

        If your data is not valid you can call `.errors` to retrieve your error.
        """
        self.__check_formulary_data

        # define everything we are gonna use while validating and saving the data
        self.user = UserExtended.objects.filter(id=self.user_id).first()
        self.form = Form.objects.filter(
            form_name=self.form_name, 
            group__company_id=self.company_id
        ).first()
        self.sections = Form.objects.filter(
            depends_on__form_name= self.form_name, 
            depends_on__group__company_id=self.company_id, 
            enabled=True
        )
        self.fields = Field.objects.filter(
            form__depends_on__form_name= self.form_name,
            form__id__in=self.sections,
            form__enabled=True,
            enabled=True
        )

        self.formulary_data = self.clean_data(self.formulary_data)

        self.validated = True
        return self.formulary_data_is_valid(self.formulary_data)        

    @transaction.atomic
    def save(self, files):
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

        Args:
            files (list(MultiParseObject)): A list with all of the files

        Raises:
            AssertionError: [description]

        Returns:
            [type]: [description]
        """
        self.__check_formulary_data

        if not hasattr(self, 'validated'):
            raise AssertionError('You should call `.is_valid()` method before trying to save the data.')
        
        self.files = files

        formulary_instance, __ = DynamicForm.objects.update_or_create(
            id=self.formulary_data.form_data_id,
            defaults={
                'form': self.form,
                'user_id': self.user_id,
                'company_id': self.company_id
            }
        )

        for section in self.formulary_data.get_sections:
            section_instance, __ = DynamicForm.objects.update_or_create(
                id=section.section_data_id, 
                defaults={
                    'form_id': section.section_id,
                    'user_id': self.user_id,
                    'company_id': self.company_id,
                    'depends_on': formulary_instance
                }
            )

            for field_value in section.get_field_values:
                field = self.fields.filter(name=field_value.field_name).first()
                form_value, __ = FormValue.objects.update_or_create(id=field_value.field_value_data_id,
                    defaults={
                        'field': field,
                        'field_type': field.type,
                        'company_id': self.company_id,
                        'date_configuration_date_format_type': field.date_configuration_date_format_type,
                        'period_configuration_period_interval_type': field.period_configuration_period_interval_type,
                        'number_configuration_number_format_type': field.number_configuration_number_format_type,
                        'formula_configuration': field.formula_configuration,
                        'form_field_as_option': field.form_field_as_option if field.type.type == 'form' else None,
                        'value': field_value.value,
                        'form': section_instance
                    }
                )
                self.add_saved_field_value_to_post_process(section_instance, form_value)

        self.post_save(self.formulary_data) 
        # updates the pre_notifications
        PreNotificationService.update(self.company_id)
        return formulary_instance
