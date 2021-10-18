from reflow_server.formulary.models import Form


class APIService:
    def __init__(self, company_id, user_id):
        self.company_id = company_id
        self.user_id = user_id

    def validate_formulary_name(self, form_name):
        return Form.data_.exists_form_name_of_company_id(form_name, self.company_id)

    def validate_data(self, form_name, data):
        """
        Validates the data transforming the data with the reflow_server.data.services.formulary.data.FormularyData
        class and the validates with the FormularyService object and then saves the data.

        Args:
            form_name (str) - The form_name of the main formulary, not from a section. (has depends_on as None)
            data (dict) - This is the data recieved from the API.
        """
        pass
