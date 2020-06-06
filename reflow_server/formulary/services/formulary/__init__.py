from reflow_server.formulary.services.formulary.data import FormularyData


class FormularyService(PostSave, PreSave):
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name

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

        Returns:
            FormularyData: The object for you which you can insert sections and field_vales
        """
        self.formulary_data = FormularyData(form_data_id)
        return self.formulary_data

    @property
    def __check_formulary_data(self):
        if not hasattr('formulary_data', self):
            raise AssertionError('You should call `.add_formulary_data()` method after calling '
                                 'the method you are trying to call')

