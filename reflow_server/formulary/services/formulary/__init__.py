from reflow_server.formulary.models import Form, Field, FormValue, DynamicForm
from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.formulary.services.formulary.data import FormularyData
from reflow_server.formulary.services.formulary.pre_save import PreSave
from reflow_server.formulary.services.formulary.post_save import PostSave


class FormularyService(PreSave):
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name
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

    def add_formulary_data(self, form_data_id=None):
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
            instance (reflow_server.formulary.models.DynamicForm, optional): The instance of the formulary
                                                                             if you are editing a formulary
                                                                             (default as None)
        Returns:
            FormularyData: The object for you which you can insert sections and field_vales
        """
        self.formulary_data = FormularyData(form_data_id)
        return self.formulary_data

    @property
    def __check_formulary_data(self):
        if not hasattr('formulary_data', self):
            raise AssertionError('You should call `.add_formulary_data()` method before calling '
                                 'the method you are trying to call')

    def is_valid(self):
        """
        Cleans the data (the internal data, not outside, we don't clean the data on your serializer or whatever directly)
        and validates the formulary data.

        If your data is not valid you can call `.errors` to retrieve your error.
        """
        self.validated = True
        self.__check_formulary_data

        self.formulary_data = self.clean_data(self.formulary_data)
        return self.formulary_data_is_valid(self.formulary_data)        

    def save(self):
        self.__check_formulary_data
    
        if not hasattr('validated', self):
            raise AssertionError('You should call `.is_valid()` method before trying to save the data.')
        
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

        self.post_save() 
        # updates the pre_notifications
        PreNotificationService.update(self.company_id)
        return formulary_instance
