from reflow_server.data.models import DynamicForm
from reflow_server.formulary.models import Form
from reflow_server.data.services.formulary.data import FormularyData

import uuid


class APIException(Exception):
    def __init__(self, reason, description=''):
        self.reason = reason 
        self.description = description


class APIService:
    def __init__(self, company_id, user_id, form_record_id=None):
        self.company_id = company_id
        self.user_id = user_id
        self.form_record_id = form_record_id


    def validate(self, form_name, data):
        try:
            self.__validate_data(form_name, data)
            return True
        except APIException as apie:
            return False
    
    def __validate_data(self, form_name, data):
        """
        Validates the data transforming the data with the reflow_server.data.services.formulary.data.FormularyData
        class and the validates with the FormularyService object and then saves the data.

        Args:
            form_name (str) - The form_name of the main formulary, not from a section. (has depends_on as None)
            data (dict) - This is the data recieved from the API.
        """
        formulary = Form.data_.form_by_form_name_of_company_id(form_name, self.company_id)
        record_uuid = str(uuid.uuid4())

        if self.form_record_id:
            formulary_record = DynamicForm.objects.filter(id=self.form_record_id, depends_on__isnull=True).first()
            if formulary_record == None:
                raise APIException('invalid_record_id')
            else:
                record_uuid = formulary_record.uuid
        if formulary:
            formulary_data = FormularyData(record_uuid, self.form_record_id)
            formulary_data.add_section_data()
        else:
            raise APIException('invalid_formulary')
