from reflow_server.authentication.models import UserExtended
from reflow_server.data.models import DynamicForm, FormValue
from reflow_server.formulary.models import Form, Field
from reflow_server.data.services.formulary import FormularyDataService

from datetime import datetime
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
        self.error = {}

    def validate(self, form_name, data):
        """
        Validates the data transforming the data with the reflow_server.data.services.formulary.data.FormularyData
        class and the validates with the FormularyService object and then saves the data.

        Args:
            form_name (str) - The form_name of the main formulary, not from a section. (has depends_on as None)
            data (dict) - This is the data recieved from the API.
        """
        try:
            formulary = Form.data_.form_by_form_name_of_company_id(form_name, self.company_id)
            if formulary:
                self.formulary_data_service = self.__transform_data(form_name, data)
                if not self.formulary_data_service.is_valid():
                    raise APIException(self.formulary_data_service.errors['reason'], json.loads(self.formulary_data_service.errors))
            else:
                raise APIException('invalid_formulary')
            return True
        except APIException as apie:
            self.error = {
                'reason': apie.reason,
                'description': apie.description
            }
            return False
        
    def save(self):
        return self.formulary_data_service.save()

    def __transform_data(self, form_name, data):
        """
        Yeah, i know the performance here is not really good, the performance depends on the number of sections and number of fields
        in the data recieved. On the long run we might transfer all of this code to the front-end so it can serve as the middleman for the api
        without affecting the performance of the backend at all, the idea is that the api will just call the backend to save the data but all of the
        validation will be done in the front directly

        For that we need to setup redis in the application for better caching of the data.

        Args:
            form_name (str): The formulary_name where you want to save the data
            data (dict): The actual data.

        Returns:
            reflow_server.data.services.formulary.FormularyDataService: Returns the formulary service with the formatted data.
        """
        # section_ids_to_ignore and form_value_ids_to_ignore is for the case when we are updating a formulary data.
        # if you look closely in the API you will see that the user does not set the sectionId neither the form_value_id when updating
        # a existing record. So we evaluate this automatically. The idea is simple. When the user is updating we get all of the sections
        # and form_values and then for each section we pass the sectionId and for each value the form_value_id. When we finish, we will effectively
        # update the data considering a number of section_ids and form_value_ids. If any of them was not attributed, we will remove from the database.
        section_ids_to_ignore = []
        form_value_ids_to_ignore = []
        formulary_data_service = FormularyDataService(self.user_id, self.company_id, form_name)
        
        formulary_data = formulary_data_service.add_formulary_data(str(uuid.uuid4()), self.form_record_id)

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
                    if isinstance(data[section_label_name], dict):
                        data[section_label_name] = [data[section_label_name]]

                    for section_record in data[section_label_name]:
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
                        
                        field_label_names = section_record.keys()
                        for field_label_name in field_label_names:
                            field_name_type_and_id = Field.objects.filter(label_name=field_label_name, form_id=section_id).values(
                                'name', 
                                'type__type', 
                                'date_configuration_date_format_type__format',
                                'number_configuration_number_format_type__decimal_separator',
                                'id'
                            ).first()
                            if field_name_type_and_id:
                                field_name = field_name_type_and_id['name']
                                field_id = field_name_type_and_id['id']
                                field_type = field_name_type_and_id['type__type']
                                field_date_format = field_name_type_and_id['date_configuration_date_format_type__format']
                                field_number_decimal_separator = field_name_type_and_id['number_configuration_number_format_type__decimal_separator']

                                values = section_record[field_label_name]
                                if not isinstance(values, list):
                                    values = [values]

                                for value in values:
                                    if field_type == 'date' and value not in ['', None]:
                                        try:
                                            formated_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z"), 
                                        except ValueError as ve:
                                            formated_datetime = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
                                        value = datetime.strftime(
                                            formated_datetime, 
                                            field_date_format
                                        )
                                    elif field_type == 'number' and value not in ['', None]:
                                        value = str(value).replace('.', field_number_decimal_separator)
                                    elif field_type == 'user' and value not in ['', None] and isinstance(value, str) and not value.isdigit():
                                        value = UserExtended.data_.user_id_by_email_and_company_id(value, self.company_id)
                                        if value == None:
                                            value = ''
                                        else:
                                            value = str(value)
                                    field_value_data = section_data.add_field_value(field_id, field_name, value)

                                    if section_data.section_data_id:
                                        form_value_id = FormValue.data_.form_value_id_by_section_record_id_and_field_id_excluding_form_value_ids(
                                            section_data.section_data_id,
                                            field_id,
                                            form_value_ids_to_ignore
                                        )
                                        if form_value_id:
                                            field_value_data.field_value_data_id.form_value_id
                                            form_value_ids_to_ignore.append(form_value_id)
                            else:
                                raise APIException('invalid_field_name', json.loads({'label_name': section_label_name, 'type': section_type_name}))
                else:
                    raise APIException('invalid_structure_for_section', json.loads({'label_name': section_label_name, 'type': section_type_name}))
            else:
                raise APIException('invalid_section_name', section_label_name)

        return formulary_data_service
        