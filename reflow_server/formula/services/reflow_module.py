
from django.conf import settings

from reflow_server.data.models import DynamicForm, FormValue
from reflow_server.data.services.representation import RepresentationService
from reflow_server.data.services.formulary import FormularyDataService
from reflow_server.formulary.models import Form, Field
from reflow_server.core.utils.asynchronous import RunAsyncFunction
from reflow_server.authentication.models import UserExtended

from datetime import datetime
import uuid


class ReflowModuleServiceException(Exception):
    def __init__(self, reason, description=''):
        self.reason = reason
        self.description = description
        super().__init__(reason)

class ReflowModuleService:
    def __init__(self, company_id, user_id, dynamic_form_id=None, variables=dict()):
        self.company_id = company_id
        self.user_id = user_id
        self.dynamic_form_id = dynamic_form_id
        self.variables = variables
        self.cached_formulary = {}
        self.cached_sections = {}
        self.cached_fields = {}
        
    def __handle_field_values_when_creating_or_updating_record(self, section_data, section_instance_id, field_label_name, values):
        field_label_name_and_section_instance_id = f'{field_label_name}_{section_instance_id}'
        if field_label_name_and_section_instance_id in self.cached_fields:
            field = self.cached_fields[field_label_name_and_section_instance_id]
        else:
            field = Field.objects.filter(label_name=field_label_name, form_id=section_instance_id).values(
                'id', 
                'name', 
                'type__type', 
                'date_configuration_date_format_type_id', 
                'date_configuration_date_format_type__format',
                'number_configuration_number_format_type_id',
                'form_field_as_option_id'
            ).first()
            self.cached_fields[field_label_name_and_section_instance_id] = field
    
        if not isinstance(values, list):
            values = [values]
            
        if field and len(values) > 0:
            representation_service = RepresentationService(
                field_type=field['type__type'],
                date_format_type_id=field['date_configuration_date_format_type_id'],
                number_format_type_id=field['number_configuration_number_format_type_id'],
                form_field_as_option_id=field['form_field_as_option_id']
            )

            if field['type__type'] == 'multi_option':
                for value in values:
                    section_data.add_field_value(field['id'], field['name'], value)
            elif field['type__type'] == 'number':
                if isinstance(values[0], int) or isinstance(values[0], float):
                    value = str(values[0] * settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT).split('.')[0]
                    value = representation_service.representation(value)
                    section_data.add_field_value(field['id'], field['name'], value)
                else:
                    raise ReflowModuleServiceException('invalid_value_for_number')
            elif field['type__type'] == 'date':
                if isinstance(values[0], datetime):
                    value = values[0].strftime(field['date_configuration_date_format_type__format'])
                    value = representation_service.representation(value)
                    section_data.add_field_value(field['id'], field['name'], value)
                else:
                    raise ReflowModuleServiceException('invalid_value_for_date')
            elif field['type__type'] == 'form':
                field_ids_that_are_a_form_field_type_variable_from_the_formula = Field.objects.filter(
                    id__in=self.variables.keys(),
                    type__type='form'
                ).values_list('id', flat=True)
                probably_the_field_original_value = None
                for field_id in field_ids_that_are_a_form_field_type_variable_from_the_formula:
                    variable_data = self.variables.get(field_id, None)
                    is_variable_data_the_same_value_as_the_value_provided = variable_data and (variable_data.cleaned == values[0] \
                        or variable_data.cleaned[1:-1] == values[0])
                    if is_variable_data_the_same_value_as_the_value_provided:
                        probably_the_field_original_value = variable_data.original[0]
                        break
                
                if self.dynamic_form_id:
                    if probably_the_field_original_value:
                        section_data.add_field_value(field['id'], field['name'], probably_the_field_original_value)
                    else:
                        section_data.add_field_value(field['id'], field['name'], values[0])
                else:
                    section_data.add_field_value(field['id'], field['name'], values[0])
            elif field['type__type'] == 'user':
                splitted_name = values[0].split(' ', 1)
                first_name = splitted_name[0]
                last_name = splitted_name[1] if len(splitted_name) > 1 else ''
                user_id = UserExtended.objects.filter(first_name=first_name, last_name=last_name, company_id=self.company_id)\
                    .values_list('id', flat=True)\
                    .first()\
                    
                if user_id:
                    section_data.add_field_value(field['id'], field['name'], str(user_id))
                else:
                    section_data.add_field_value(field['id'], field['name'], values[0])
            else:
                section_data.add_field_value(field['id'], field['name'], values[0])
        else:
            if len(values) < 0:
                raise ReflowModuleServiceException('values_should_not_be_empty')
            else:
                raise ReflowModuleServiceException('invalid_field')

    def create_record(self, template_name, page_name, data):
        """
        I don't like it much, it's bloated with logic here, because reflow is actually a really complex piece of software and not 
        a so easy one.

        Multi-sections are handled as lists and sections are handled as dicts.

        Be aware that validate EVERYTHING is Extremely important here, if an error is thrown we need to show it to the user
        in the front-end. If you don't specify any error the user will only recieve 'formula not valid' in the front-end.

        Args:
            template_name (str): The name of the Group of where the page/formulary is in.
            page_name (str): The label name of the page
            data (dict): This follows the following format
            >>> {
                "Name Of Section Label Name": {
                    "Name of field": ["value you want to add"],
                    "Name of multi_option field": ["Value you want to add 1", "Value you want to add 2"]
                },
                "Name of Multi Section Label Name": [
                    {
                        "Name of field": ["Value to add in the multi section"]
                    }
                ]
            }

        Raises:
            ReflowModuleServiceException: invalid_page_name - When the page name provided doesn't exist for the company
            ReflowModuleServiceException: invalid_section_name - When the section name provided doesn't exist for the particular page/formulary
            ReflowModuleServiceException: invalid_value_type_for_section_type - When the section is a multi-section it should be a list, otherwise it should be a form
            ReflowModuleServiceException: items_of_multi_section_should_be_a_dict - When it is a multi-section, all of the items should be a dict and not of any other type
            ReflowModuleServiceException: invalid_field - The field does not exist for the section provided.

        Returns:
            int: Returns the id of the instance added, if you want to make use of this you can.
        """
        formulary_group_name_label_name_and_company_id = '{}_{}_{}'.format(template_name, page_name, self.company_id)
        if formulary_group_name_label_name_and_company_id not in self.cached_formulary:
            main_formulary = Form.objects.filter(
                group__name=template_name, 
                label_name=page_name, 
                group__company_id=self.company_id, 
                depends_on__isnull=True
            ).values(
                'id',
                'form_name'
            ).first()
            self.cached_formulary[formulary_group_name_label_name_and_company_id] = main_formulary
        else:
            main_formulary = self.cached_formulary[formulary_group_name_label_name_and_company_id]

        if main_formulary:
            formulary_service = FormularyDataService(self.user_id, self.company_id, main_formulary['form_name'])
            formulary_data = formulary_service.add_formulary_data(str(uuid.uuid4()))
            for section_name, section_field_values in data.items():
                section_name_company_id_and_formulary_id = '{}_{}_{}'.format(section_name, self.company_id, main_formulary['id'])
                if section_name_company_id_and_formulary_id not in self.cached_sections:
                    section = Form.objects.filter(
                        label_name=section_name, 
                        depends_on__group__company_id=self.company_id, 
                        depends_on_id=main_formulary['id']
                    ).values(
                        'id',
                        'type__type'
                    ).first()
                    self.cached_sections[section_name_company_id_and_formulary_id] = section
                else:
                    section = self.cached_sections[section_name_company_id_and_formulary_id]
                if section:
                    section_data = formulary_data.add_section_data(
                        section_id=section['id'], 
                        uuid=str(uuid.uuid4()) 
                    )
                    if section['type__type'] == 'form' and isinstance(section_field_values, dict):
                        for field_label_name, values in section_field_values.items():
                            self.__handle_field_values_when_creating_or_updating_record(section_data, section['id'], field_label_name, values)

                    elif section['type__type'] == 'multi-form' and (isinstance(section_field_values, list) or isinstance(section_field_values, dict)):
                        if isinstance(section_field_values, dict):
                            section_field_values = [section_field_values]
                        for multi_section_data_item in section_field_values:
                            if isinstance(multi_section_data_item, dict):
                                for field_label_name, values in multi_section_data_item.items():
                                    self.__handle_field_values_when_creating_or_updating_record(section_data, section['id'], field_label_name, values)
                            else:
                                raise ReflowModuleServiceException('items_of_multi_section_should_be_a_dict')                  
                    else:
                        raise ReflowModuleServiceException('invalid_value_type_for_section_type')                  
                else:
                    raise ReflowModuleServiceException('invalid_section_name')
            if formulary_service.is_valid():
                formulary_instance = formulary_service.save()
                return formulary_instance.id
            else:
                raise ReflowModuleServiceException(formulary_service.errors['reason'])
        else:
            raise ReflowModuleServiceException('invalid_page_name')
            
            