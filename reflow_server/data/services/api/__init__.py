from reflow_server.data.models import DynamicForm
from reflow_server.formulary.models import Form, Field
from reflow_server.data.services.formulary.data import FormularyData

import uuid
import json


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

    def __transform_data(self, form_name, data):
        section_ids_to_ignore = []
        formulary_data = FormularyData(str(uuid.uuid4()), self.form_record_id)

        if self.form_record_id:
            formulary_record_uuid = DynamicForm.data_.main_form_uuid_by_form_record_id_and_company_id(self.form_record_id, self.company_id)
            if formulary_record_uuid == None:
                raise APIException('invalid_record_id', self.form_record_id)
            else:
                formulary_data.uuid = formulary_record_uuid

        section_label_names = data.keys()
        for section_label_name in section_label_names:
            section_id_and_type_name = Form.data_.section_type_and_id_by_label_name_main_form_name_and_company_id(section_label_name, form_name, self.company_id)
            
            if section_id_and_type_name:
                section_id = section_id_and_type_name['id']
                section_type_name = section_id_and_type_name['type__type']

                is_valid_unique_section = section_type_name == 'form' and isinstance(data[section_label_name], dict)
                is_valid_multi_section = section_type_name == 'multi-form' and isinstance(data[section_label_name], list)

                if is_valid_unique_section or is_valid_multi_section:
                    section_data = formulary_data.add_section_data(section_id, str(uuid.uuid4()))
                    if self.form_record_id:
                        section_record_id_and_uuid = DynamicForm.data_.section_record_id_and_uuid_by_section_id_and_main_form_id_excluding_ids_and_ordering_by_udated_at(
                            section_id,
                            self.form_record_id,
                            section_ids_to_ignore
                        )
                        if section_record_id_and_uuid:
                            section_record_id = section_record_id_and_uuid['id']
                            section_record_uuid = section_record_id_and_uuid['uuid']

                            section_ids_to_ignore.append(section_record_id)
                            section_data.section_uuid = section_record_uuid
                            section_data.section_data_id = section_record_id
                    field_label_names = data[section_label_name].keys()
                    for field_label_name in field_label_names:
                        field_name_and_id = Field.objects.filter(label_name=field_label_name, form_id=section_id).values('name', 'id').first()
                        if field_name_and_id:
                            field_name = field_name_and_id['name']
                            field_id = field_name_and_id['id']

                            # TODO: Translate fields
                        else:
                            raise APIException('invalid_field_name', json.loads({'label_name': section_label_name, 'type': section_type_name}))

                else:
                    raise APIException('invalid_structure_for_section', json.loads({'label_name': section_label_name, 'type': section_type_name}))
            else:
                raise APIException('invalid_section_name', section_label_name)

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

        self.__transform_data(form_name, data)
        if formulary:
            formulary_data = FormularyData(record_uuid, self.form_record_id)
            formulary_data.add_section_data()
        else:
            raise APIException('invalid_formulary')
