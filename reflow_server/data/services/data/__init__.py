from reflow_server.data.services.data.sort import DataSort
from reflow_server.data.services.data.search import DataSearch
from reflow_server.data.models import FormValue, DynamicForm
from reflow_server.formulary.models import OptionAccessedBy, Field, FieldOptions, FormAccessedBy
from reflow_server.authentication.models import UserExtended


class DataService(DataSort, DataSearch):
    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id
    
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
        
        form_ids_a_user_has_access_to = FormAccessedBy.objects.filter(user=self.user_id).values_list('form_id', flat=True).distinct()
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
        ).values('id', 'name', 'type__type', 'form_field_as_option')

        # fields become a dict with each name becoming each key of the dict.
        self._fields = {
            field['name']: {
                'id': field['id'],
                'type': field['type__type'],
                'form_field_as_option_id': field['form_field_as_option']
            } for field in self._fields
        }

        if from_date and to_date:
            self._data = DynamicForm.objects.filter(
                company_id=self.company_id, 
                updated_at__range=[from_date, to_date],
                form_id=form_id
            ).order_by('-updated_at')

        else:
            self._data = DynamicForm.objects.filter(
                company_id=self.company_id, 
                form_id=form_id
            ).order_by('-updated_at')

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
        user = UserExtended.objects.filter(id=self.user_id).first()
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

                all_form_values = FormValue.objects.filter(
                    form__depends_on__in=self._data,
                    field__in=list(options_by_field.keys()),
                    field_type__type__in=['option', 'multi_option'],
                    company_id=self.company_id
                ).order_by('form__depends_on')

                forms_to_ignore = list()
                for (value, field_id, field_type, form_depends_on) in all_form_values.values_list('value', 'field_id', 'field__type__type', 'form__depends_on'):
                    if field_id in options_by_field and value not in options_by_field[field_id]+[''] and field_id in field_options_by_field and value in field_options_by_field[field_id]:
                        forms_to_ignore.append(form_depends_on)
                self._data = self._data.exclude(id__in=forms_to_ignore)
