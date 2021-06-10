from django.conf import settings

from reflow_server.data.models import FormValue
from reflow_server.authentication.models import UserExtended
from reflow_server.data.services.data.data import FieldData
from reflow_server.data.services.representation import RepresentationService

from datetime import datetime


class SearchItem:
    def __init__(self, field_name, value, exact):
        self.field_name = field_name
        self.value = value
        self.exact = exact == "1"
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def convert_search_data(serach_data):
        search_objects = list()
        for search in serach_data:
            [(field_name, (field_value, search_exact))] = search.items()
            search_objects.append(SearchItem(field_name, field_value, search_exact))
        return search_objects
    # ------------------------------------------------------------------------------------------


############################################################################################
class DataSearch:
    # ------------------------------------------------------------------------------------------
    def __search_exact(self, search_item, value=None):
        # Searchs for the exact value or parcial value, parcial also ignores the case
        value = value if value else search_item.value 
        print(value)
        print(type(value))
        if search_item.exact:
            return {
                'value': value
            }
        else:
            return {
                'value__icontains': value
            }
    # ------------------------------------------------------------------------------------------
    def _search(self, search_keys):
        """
        Used for searching the keys in the forms, it's a loop so all the filters are satisfied.
        The search keys are a list containing dicts for each key to filter, the key is the field name,
        the value is a tuple containing both the value to filter and 0 or 1 to check if it's an exact search.
        Exact search is searching the hole value not searching parts of it.

        Args:
            search_keys (list(dict)):as explained above must be like:
            >>> [
                { 
                    test_key: (test_value, 0) 
                }
            ]
        """
        search_data = SearchItem.convert_search_data(search_keys) 

        form_ids_to_filter = list(self._data.values_list('id', flat=True))
        for to_search in search_data:

            if to_search.field_name in self._fields:
                field_data = self._fields[to_search.field_name]

                form_ids_to_filter = self.__search(to_search, field_data, form_ids_to_filter)
                """
                field_data = self._fields[to_search.field_name]

                handler = getattr(self, '_search_%s' % field_data.field_type, None)
                if handler:
                    form_ids_to_filter = handler(to_search, field_data, form_ids_to_filter)
                else:
                    form_ids_to_filter = list(
                        FormValue.data_.form_depends_on_ids_for_search_all_field_types(
                            company_id=self.company_id, 
                            depends_on_forms=list(form_ids_to_filter),
                            field_id=field_data.id,
                            field_type=field_data.field_type,
                            search_value_dict=self.__search_exact(to_search)
                        )
                    )
                """

        self._data = self._data.filter(company_id=self.company_id, id__in=form_ids_to_filter)
    # ------------------------------------------------------------------------------------------
    def __search(self, search_item, field_data, form_ids_to_filter):
        """
        Responsible for making the search on each item and dispatching the handler for specific fields or
        handling itself a default and generic search.

        Args:
            search_item (dict): {
                field_name: (value_to_search, 0 or 1)
            }
            form_ids_to_filter (list(int)): A list of FormValue instance ids, this is used for filtering so we 
            can transverse every filter.

        Returns:
            list(int): Returns the filtered list of FormValue instance ids.
        """
        handler = getattr(self, '_search_%s' % field_data.field_type, None)
        if handler:
            return handler(search_item, field_data, form_ids_to_filter)
        else:
            return list(
                FormValue.data_.form_depends_on_ids_for_search_all_field_types(
                    company_id=self.company_id, 
                    depends_on_forms=list(form_ids_to_filter),
                    field_id=field_data.id,
                    field_type=field_data.field_type,
                    search_value_dict=self.__search_exact(search_item)
                )
            )
    # ------------------------------------------------------------------------------------------
    def _search_date(self, search_item, field_data, form_ids_to_filter):
        """
        When the user is trying to filter dates, if he types 06/08/2020 - 06/08/2020
        we assume he is trying to filter from the same date so it considers the following range:

        From 2020-08-06 00:00:00  TO 2020-06-06 23:59:59

        Otherwise if he types 06/08/2020 - 07/08/2020 it is

        From 2020-08-06 00:00:00  TO 2020-06-07 23:59:59
        """
        representation_service = RepresentationService(
            field_data.field_type, 
            field_data.date_format_type_id,
            field_data.number_format_type_id,
            field_data.form_field_as_option_id
        )
        split_search_value = search_item.value.split(' - ')
        start_date = representation_service.to_internal_value(split_search_value[0].split(' ')[0]) 
        end_date = representation_service.to_internal_value(split_search_value[1].split(' ')[0])

        start_date = datetime.strptime(start_date, settings.DEFAULT_DATE_FIELD_FORMAT)
        end_date = datetime.strptime(end_date, settings.DEFAULT_DATE_FIELD_FORMAT).replace(hour=23, minute=59, second=59) 

        return list(
                FormValue.data_.form_depends_on_ids_for_search_date_field_types(
                    company_id=self.company_id, 
                    depends_on_forms=list(form_ids_to_filter), 
                    field_id=field_data.id, 
                    field_type=field_data.field_type,
                    start_date=start_date,
                    end_date=end_date
                )
            )
    # ------------------------------------------------------------------------------------------
    def _search_number(self, search_item, field_data, form_ids_to_filter):
        representation_service = RepresentationService(
            field_data.field_type, 
            field_data.date_format_type_id,
            field_data.number_format_type_id,
            field_data.form_field_as_option_id
        )

        value = representation_service.to_internal_value(search_item.value)

        return list(
            FormValue.data_.form_depends_on_ids_for_search_all_field_types(
                company_id=self.company_id, 
                depends_on_forms=list(form_ids_to_filter),
                field_id=field_data.id,
                field_type=field_data.field_type,
                search_value_dict=self.__search_exact(search_item, value)
            )
        )
    # ------------------------------------------------------------------------------------------
    def _search_form(self, search_item, field_data, form_ids_to_filter):
        return list(
            FormValue.data_.form_depends_on_ids_for_search_form_field_types(
                company_id=self.company_id, 
                depends_on_forms=list(form_ids_to_filter), 
                field_id=field_data.id, 
                field_type=field_data.field_type,
                form_field_as_option_id=field_data.form_field_as_option_id,
                search_value_dict=self.__search_exact(search_item)
            )
        )
    # ------------------------------------------------------------------------------------------
    def _search_user(self, search_item, field_data, form_ids_to_filter):
        first_name = search_item.value.split(' ')[0]
        last_name = search_item.value.split(' ')[1] if len(search_item.value.split(' ')) > 1 else None
        search_value_dict = self.__search_exact(search_item)
        
        if not last_name:
            if '__icontains' in search_value_dict.keys():
                search_dict = {
                    'first_name__icontains': first_name
                }
            else:
                search_dict = {
                    'first_name': first_name
                }

        else:
            if '__icontains' in search_value_dict.keys():
                search_dict = {
                    'first_name__icontains': first_name,
                    'last_name__icontains': last_name
                }
            else:
                search_dict = {
                    'first_name': first_name,
                    'last_name': last_name
                }

        search_values = list(
            UserExtended.data_.user_ids_for_search_by_search_value_and_company_id(
                self.company_id,
                search_dict
            )
        )

        return list(
            FormValue.data_.form_depends_on_ids_for_search_user_field_types(
                company_id=self.company_id, 
                depends_on_forms=list(form_ids_to_filter), 
                field_id=field_data.id, 
                field_type=field_data.field_type,
                search_user_ids=search_values
            )
        )
    # ------------------------------------------------------------------------------------------
    def _search_formula(self, search_item, field_data, form_ids_to_filter):
        latest_form_value = FormValue.data_.latest_form_value_field_type_by_field_id(field_data.id)
        if latest_form_value:
            field_data = FieldData(
                field_data.id, 
                latest_form_value.field_type.type, 
                latest_form_value.date_configuration_date_format_type_id,
                latest_form_value.number_configuration_number_format_type_id,
                latest_form_value.form_field_as_option_id
            )   
        else:
            field_data = FieldData(
                field_data.id, 
                '', 
                field_data.date_format_type_id,
                field_data.number_format_type_id,
                field_data.form_field_as_option_id
            )  
        return self.__search(search_item, field_data, form_ids_to_filter)
