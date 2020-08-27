from reflow_server.data.models import FormValue
from reflow_server.authentication.models import UserExtended

from datetime import datetime, timedelta


class SearchItem:
    def __init__(self, field_name, value, exact):
        self.field_name = field_name
        self.value = value
        self.exact = exact == "1"

    @staticmethod
    def convert_search_data(serach_data):
        search_objects = list()
        for search in serach_data:
            [(field_name, (field_value, search_exact))] = search.items()
            search_objects.append(SearchItem(field_name, field_value, search_exact))
        return search_objects


class DataSearch:
    def __search_exact(self, search_item):
        # Searchs for the exact value or parcial value, parcial also ignores the case
        if search_item.exact:
            return {
                'value': search_item.value
            }
        else:
            return {
                'value__icontains': search_item.value
            }
    
    def _search(self, search_keys):
        """
        Used for searching the keys in the forms, it's a loop so all the filters are satisfied.
        The search keys are a list containing dicts for each key to filter, the key is the field name,
        the value is a tuple containing both the value to filter and 0 or 1 to check if it's an exact search.
        Exact search is searching the hole value not searching parts of it.

        Args:
            search_keys {list(dict)}- as explained above must be like [{ test_key: (test_value, 0) }]
        
        return all the forms filtered
        """
        search_data = SearchItem.convert_search_data(search_keys) 

        form_ids_to_filter = list(self._data.values_list('id', flat=True))
        for to_search in search_data:
            field_data = self._fields[to_search.field_name]

            handler = getattr(self, '_search_%s' % field_data['type'], None)
            if handler:
                form_ids_to_filter = handler(to_search, field_data, form_ids_to_filter)
            else:
                form_ids_to_filter = list(
                    FormValue.data_.form_depends_on_ids_for_search_all_field_types(
                        company_id=self.company_id, 
                        depends_on_forms=list(form_ids_to_filter),
                        field_id=field_data['id'],
                        field_type=field_data['type'],
                        search_value_dict=self.__search_exact(to_search)
                    )
                )

        self._data = self._data.filter(company_id=self.company_id, id__in=form_ids_to_filter)

    def _search_date(self, search_item, field_data, form_ids_to_filter):
        """
        When the user is trying to filter dates, if he types 06/08/2020 - 06/08/2020
        we assume he is trying to filter from the same date so it considers the following range:

        From 2020-08-06 00:00:00  TO 2020-06-06 23:59:59

        Otherwise he is he types 06/08/2020 - 07/08/2020

        From 2020-08-06 00:00:00  TO 2020-06-07 23:59:59
        """
        search_values = list()
        split_search_value = search_item.value.split(' - ')
        start_date = datetime.strptime(split_search_value[0].split(' ')[0], field_data['date_configuration_date_format_type_format'].split(' ')[0]) 
        end_date = datetime.strptime(split_search_value[1].split(' ')[0] + ' 23:59:59', '{} %H:%M:%S'.format(field_data['date_configuration_date_format_type_format'].split(' ')[0])) 

        return list(
                FormValue.data_.form_depends_on_ids_for_search_date_field_types(
                    company_id=self.company_id, 
                    depends_on_forms=list(form_ids_to_filter), 
                    field_id=field_data['id'], 
                    field_type=field_data['type'],
                    start_date=start_date,
                    end_date=end_date
                )
            )
    
    def _search_form(self, search_item, field_data, form_ids_to_filter):
        return list(
            FormValue.data_.form_depends_on_ids_for_search_form_field_types(
                company_id=self.company_id, 
                depends_on_forms=list(form_ids_to_filter), 
                field_id=field_data['id'], 
                field_type=field_data['type'],
                form_field_as_option_id=field_data['form_field_as_option_id'],
                search_value_dict=self.__search_exact(search_item)
            )
        )
        
    def _search_user(self, search_value, field_data, form_ids_to_filter):
        first_name = search_value.split(' ')[0]
        last_name = search_value.split(' ')[1] if len(search_value.split(' ')) > 1 else None
        if not last_name:
            search_values = list(
                UserExtended.objects.filter(
                    first_name__icontains=first_name, 
                    company_id=self.company_id
                ).values_list('id', flat=True)
            )
        else:
            search_values = list(
                UserExtended.objects.filter(
                    first_name__icontains=first_name, 
                    last_name__icontains=last_name, 
                    company_id=self.company_id
                ).values_list('id', flat=True)
            )

        return list(
            FormValue.data_.form_depends_on_ids_for_search_user_field_types(
                company_id=self.company_id, 
                depends_on_forms=list(form_ids_to_filter), 
                field_id=field_data['id'], 
                field_type=field_data['type'],
                search_user_ids=search_values
            )
        )
