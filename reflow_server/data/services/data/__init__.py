from reflow_server.data.services.data.sort import DataSort
from reflow_server.data.services.data.search import DataSearch
from reflow_server.data.models import FormValue, DynamicForm
from reflow_server.formulary.models import OptionAccessedBy, Field, FieldOptions
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.authentication.models import UserExtended

from datetime import datetime, timedelta

class DataService(DataSort, DataSearch):
    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id
    
    @staticmethod
    def validate_and_extract_date_from_string(date):
        try:
            return datetime.strptime(date, '%d/%m/%Y')
        except ValueError as ve:
            return None
        return None

    @classmethod
    def get_user_form_data_ids_from_query_params(cls, query_params, user_id, company_id, form_id):
        """
        This is a handy function to extract the data_ids from the query_params you might recieve from the request.
        With this function you get all of the dynamic_form_ids accessed by the user for a particular form based on
        the query params you recieve in your request. This way we can mantain a common query param pattern on
        `get` and `delete` requests

        Args:
            query_params (django.Request.query_params): the query params of the request.
            user_id (int): For which user you want to extract the data.
            company_id (int): for which company of the user you are extracting the data
            form_id (int): for which form/page are you extracting the data

        Returns:
            list(int) -- Returns a list of all of the dynamic_form_ids that the user has access to from a single form_id.
        """
        data_service = cls(user_id=user_id, company_id=company_id)
        params = data_service.extract_query_parameters_from_request(query_params)

        from_date = DataService.validate_and_extract_date_from_string(query_params.get('from_date', ''))
        to_date = DataService.validate_and_extract_date_from_string(query_params.get('to_date', ''))
        
        # get the correct data to pass as parameters
        converted_search_data = data_service.convert_search_query_parameters(params['search']['field'], params['search']['value'], params['search']['exact'])
        converted_sort_data = data_service.convert_sort_query_parameters(params['sort']['field'], params['sort']['value'])
        form_data_accessed_by_user = data_service.get_user_form_data_ids_from_form_id(form_id, converted_search_data, converted_sort_data, from_date=from_date, to_date=to_date)
        return form_data_accessed_by_user

    @staticmethod
    def extract_query_parameters_from_request(query_params):
        if all([value in query_params for value in ['search_field', 'search_value', 'search_exact']]):
            search_field_query_param = query_params.getlist('search_field', list())
            search_value_query_param = query_params.getlist('search_value', list())
            search_exact_query_param = query_params.getlist('search_exact', list())
        else:
            search_field_query_param = query_params.getlist('search_field[]', list())
            search_value_query_param = query_params.getlist('search_value[]', list())
            search_exact_query_param = query_params.getlist('search_exact[]', list())

        if all([value in query_params for value in ['sort_field', 'sort_value']]):
            sort_field_query_param = query_params.getlist('sort_field', list())
            sort_value_query_param = query_params.getlist('sort_value', list())
        else:
            sort_field_query_param = query_params.getlist('sort_field[]', list())
            sort_value_query_param = query_params.getlist('sort_value[]', list())

        return {
            'search': {
                'exact': search_exact_query_param,
                'value': search_value_query_param,
                'field': search_field_query_param
            },
            'sort': {
                'value': sort_value_query_param,
                'field': sort_field_query_param
            }
        }

    @staticmethod
    def convert_sort_query_parameters(sort_field_names_list, sort_values_list):
        """
        Method for converting simple lists to list of dicts used by DataService.get_user_form_data_ids_from_form_id() method.

        Arguments:
            sort_field_names_list {list(str)} -- the list of field_names recieved on the query_parameter
            sort_values_list {list(enum('upper', 'down'))} -- the list of sort_values recieved on the query_parameter

        Raises:
            AssertionError: if your `sort_values_list` are not `upper` or `down`
            AssertionError: if your lists not have equal lengths

        Returns:
            [list(dict)] -- List of dicts to be used on .get_user_form_data_ids_from_form_id() method as sort_keys
        """
        if any([sort_value not in ['upper', 'down'] for sort_value in sort_values_list]):
            raise AssertionError('Your values must be either `upper` or `down`, '
                                 'looks like one of your values is not one of those options')
        if len(sort_values_list) != len(sort_field_names_list):
            raise AssertionError('Your `sort_field_names_list` parameter and `sort_values_list` parameter '
                                 'does not have equal lengths')
        
        formatted_sort = [{
                sort_field_names_list[index]: sort_values_list[index]
            } for index in range(0, len(sort_values_list))]

        return formatted_sort

    @staticmethod
    def convert_search_query_parameters(search_field_names_list, search_values_list, search_exact_list):
        """
        Method for converting simple lists to list of dicts used by DataService.get_user_form_data_ids_from_form_id() method.

        Arguments:
            search_field_names_list {list(str)} -- the list of field_names recieved on the query_parameter
            search_values_list {list(str)} -- list of values to search, can be complete values or parcial values
            search_exact_list {list(str)} -- You could search for the exact value (1) or search for the parcial value (0)

        Raises:
            AssertionError: if your `search_exact_list` is not value `0` or `1`
            AssertionError: if your lists not have equal lengths

        Returns:
            [list(dict)] -- List of dicts to be used on .get_user_form_data_ids_from_form_id() method as search_keys
        """
        if any([str(search_exact) not in ['1', '0'] for search_exact in search_exact_list]):
            raise AssertionError('Your search_exact values must be either `0` or `1`, '
                                 'looks like one of your values is not one of those options')
        if any(len(lst) != len(search_field_names_list) for lst in [search_values_list, search_exact_list]):
            raise AssertionError('Your `search_field_names_list` parameter, `search_values_list` parameter '
                                 'and `search_exact_list` parameter does not have equal lengths')
        formatted_search = [
            {
                search_field_names_list[index]: (
                    search_values_list[index], 
                    search_exact_list[index]
                )
            } for index in range(0, len(search_field_names_list))
        ]

        return formatted_search

    def all_form_data_a_user_has_access_to(self):
        """
        Extremally slow function for retrieving all of the forms a user has access to, don't use it,
        unless absolutely needed.

        Returns:
            list(int): list of DynamicForm ids that a user has access
        """
        all_dynamic_form_ids_a_user_has_access_to = list()
        
        form_ids_a_user_has_access_to = FormularyService(self.user_id, self.company_id).formulary_ids_the_user_has_access_to
        for form_id in form_ids_a_user_has_access_to:
            forms_data = self.get_user_form_data_ids_from_form_id(form_id)
            all_dynamic_form_ids_a_user_has_access_to = all_dynamic_form_ids_a_user_has_access_to + forms_data

        return all_dynamic_form_ids_a_user_has_access_to

    def get_user_form_data_ids_from_form_id(self, form_id, search_keys=[], sort_keys=[], from_date=None, to_date=None):
        """
        Retrieves all of the data of a formulary that a user has access to. This function already handles search, and sort.
        This function retrieves the formulary data of a single form, not from multiple forms.
        
        Arguments:
            form_id {int} -- the form_id to retrieve the user data from

        Keyword Arguments:
            search_keys {list(dict)} -- (default: {None}) -- list of fields to search, each dict on the list must be on the following format:
            >>> {
                field_name: (value_to_search, 0 or 1)
            }
            
            sort_keys {list(dict)} -- (default: {None}) -- list of fields to sort, value_to_sort must be `upper` or 'down', 
            each dict on the list must follow the format:
            >>> {
                field_name: value_to_sort
            } 

            from_date {datetime.datetime} -- The first date that the form was updated, right now only needed when
            downloading the formulary (default: {None})
            to_date {datetime.datetime} -- The last date the form was updated, right now only needed when downloading
            the formulary (default: {None})

        Returns:
            list(int) -- Returns a list of all of the dynamic_form_ids that the user has access to from a single form_id.
        """

        self._fields = Field.objects.filter(
            form__company_id=self.company_id,
            form__depends_on_id=form_id
        ).values('id', 'name', 'type__type', 'date_configuration_date_format_type__format', 'form_field_as_option')

        # fields become a dict with each name becoming each key of the dict.
        self._fields = {
            field['name']: {
                'id': field['id'],
                'type': field['type__type'],
                'date_configuration_date_format_type_format': field['date_configuration_date_format_type__format'],
                'form_field_as_option_id': field['form_field_as_option']
            } for field in self._fields
        }

        if from_date and to_date:
            self._data = DynamicForm.data_.dynamic_forms_by_company_id_form_id_between_updated_at_range_ordered_by_updated_at(
                self.company_id, 
                form_id,
                from_date, 
                to_date + timedelta(days=1)
            )

        else:
            self._data = DynamicForm.data_.dynamic_forms_by_company_id_and_form_id_orderd_by_updated_at(
                self.company_id, 
                form_id
            )

        if search_keys:
            if type(search_keys) != list or any([type(search) != dict for search in search_keys]) or any([type(list(search.values())[0]) != tuple for search in search_keys]):
                raise AssertionError('Your list of dicts must follow the following formatting: \n'
                                     '>>> { \n'
                                     '  field_name: (value_to_search, 0 or 1) \n'
                                     '} \n'
                                     '\n'
                                     'You can use the .convert_search_query_parameters() staticmethod of DataService class to convert from query parameters to this format.')
            self._search(search_keys)

        if sort_keys:
            if type(sort_keys) != list or any([type(sort) != dict for sort in sort_keys]) or any([list(sort.values())[0] not in ['upper', 'down'] for sort in sort_keys]):
                raise AssertionError('Your list of dicts must follow the following formatting: \n'
                                     '>>> { \n'
                                     '  field_name: sort_value \n'
                                     '} \n'
                                     '\n'
                                      'You can use the .convert_sort_query_parameters() staticmethod of DataService class to convert from query parameters to this format.')
            self._sort(sort_keys)

        self.__filter_by_profile_permissions(form_id)
        return list(self._data.values_list('id', flat=True))

    def __filter_by_profile_permissions(self, form_id):
        user = UserExtended.data_.user_by_user_id(self.user_id)
        if user.profile.name == 'simple_user':
            main_forms = self._data.filter(user_id=self.user_id)
        else:
            field_options = FieldOptions.objects.filter(
                    field__form__depends_on__group__company_id=self.company_id,
                    field__form__depends_on_id=form_id
                ).values('field_id', 'option')

            if not field_options:
                # If there is no field_options on this form, consequently, no filter needs to be made.
                # In this condition we return all the data to the user, like if he was an admin.
                return
            else:
                options_accessed_by_user = OptionAccessedBy.objects.filter(
                        user_id=self.user_id,
                        field_option__field__form__depends_on_id=form_id
                    ).values('field_option__field_id', 'field_option__option')

                field_options_by_field = dict()
                options_by_field = dict()

                for option in options_accessed_by_user:
                    options_by_field[option['field_option__field_id']] = options_by_field.get(
                        option['field_option__field_id'], []
                    ) + [option['field_option__option']]

                for field_option in field_options:
                    field_options_by_field[field_option['field_id']] = field_options_by_field.get(
                        field_option['field_id'], []
                    ) + [field_option['option']]

                all_form_values = FormValue.data_.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(
                    company_id=self.company_id,
                    depends_on_forms=self._data,
                    field_ids=list(options_by_field.keys()),
                    field_types=['option', 'multi_option']
                )

                forms_to_ignore = list()
                for (value, field_id, field_type, form_depends_on) in all_form_values.values_list('value', 'field_id', 'field__type__type', 'form__depends_on'):
                    if field_id in options_by_field and value not in options_by_field[field_id]+[''] and field_id in field_options_by_field and value in field_options_by_field[field_id]:
                        forms_to_ignore.append(form_depends_on)
                self._data = self._data.exclude(id__in=forms_to_ignore)
