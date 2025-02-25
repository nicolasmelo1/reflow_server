from django.db.models import Case, When
from reflow_server.data.services.data.data import FieldData

from reflow_server.data.models import FormValue
from reflow_server.authentication.models import UserExtended


class SortItem:
    def __init__(self, field_name, value):
        self.field_name = field_name
        self.value = value
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def convert_sort_data(sort_data):
        sort_objects = list()
        for sort in sort_data:
            [(field_name, field_value)] = sort.items()
            sort_objects.append(SortItem(field_name, field_value))
        return sort_objects
    # ------------------------------------------------------------------------------------------


############################################################################################
class DataSort:
    # ------------------------------------------------------------------------------------------
    def _sort(self, sort_keys):
        """
        Sorts forms queryset based on sort_keys conditions, since it can be multiple sorts we sort inside of a list, so we sort the first row, than the second field 
        and so on.
        :param sort_keys: list of dicts
        :param fields: queryset of company's fields
        :param forms: forms queryset
        """
        sort_data= SortItem.convert_sort_data(sort_keys) 
        forms_order = dict()

        # A user can have multiple sorts, so we need to norrow the sort for each sort. 
        # This is why it is on a for loop.
        for to_sort in sort_data:
            field_data = self._fields.get(to_sort.field_name, None)
            if field_data:
                order_up_or_down = 'value' if 'down' in to_sort.value else '-value'

                orderded_values_and_form_ids = self.__sort(order_up_or_down, field_data)
                
                # order_key holds the value as the key with each form_id in the list of the key
                # we filter like this because for example for `field_type` as `option`, if we have 2 options
                # only like `SP`, or `RJ`, it doesn't matter the order inside both filters, we are always narrowing 
                # our filter
                # we end up with a dict with `RJ` and `SP` keys only with a big list on each of them, 
                # when we do a second sort, we norrow the list for less values and so on.
                order_key = dict()
                for orderded_value_and_form_id in orderded_values_and_form_ids:
                    order_key[orderded_value_and_form_id['value']] = order_key.get(
                        orderded_value_and_form_id['value'], []
                    ) + [orderded_value_and_form_id['form__depends_on']]

                # check if forms_order is empty or not, we fill it in the else.
                if not forms_order:
                    forms_order = order_key

                else:
                    # each key on forms_order becomes appended by each value we filter, so for example if we filter by
                    # `region` and `status`: all of the possible values from region, becomes appended to all of the values from status
                    # if we have options like `RJ` and `SP` for regions, and `Todo` and `Done` for status we end with 4 possible keys:
                    # `RJTodo`, `RJDone`, `SPTodo`, ˜SPDone`. Each key have some forms to order so we order until number 4, one
                    # for each Key. It doesn't matter the order inside of the options as we discussed above.
                    aux_forms_order = forms_order.copy()
                    forms_order = dict()
                    for aux_forms_order_value, aux_forms_order_form_ids in aux_forms_order.items():
                        for order_key_value, order_key_form_ids in order_key.items():
                            exists_in_both_lists = [form_id for form_id in aux_forms_order_form_ids if form_id in order_key_form_ids]
                            if exists_in_both_lists:
                                aux_forms_order_value = aux_forms_order_value if aux_forms_order_value is not None else ''
                                order_key_value = order_key_value if order_key_value is not None else ''

                                forms_order[aux_forms_order_value + order_key_value] = exists_in_both_lists
                                
                order = Case(*[When(id__in=value, then=pos) for pos, value in enumerate(forms_order.values())]) if forms_order.values() else None
                if self._data and order:
                    self._data = self._data.order_by(order)
    # ------------------------------------------------------------------------------------------
    def __sort(self, order_up_or_down, field_data):
        # tries to find a handler to sort specific field_types
        # if a handler is found or not, we return the value and the formulary_id
        # this way we can give a number to each formulary_id individually. so they can be sorted.
        handler = getattr(self, '_sort_%s' % field_data.field_type, None)
        if handler:
            return handler(order_up_or_down, field_data)
        else:
            return FormValue.data_.form_depends_on_and_values_for_sort_all_field_types(
                company_id=self.company_id, 
                depends_on_forms=self._data, 
                field_id=field_data.id,
                order_by_value=order_up_or_down
            ) 
    # ------------------------------------------------------------------------------------------
    def _sort_date(self, order_up_or_down, field_data):
        return FormValue.data_.form_depends_on_and_values_for_sort_date_field_types(
            company_id=self.company_id, 
            depends_on_forms=self._data, 
            field_type=field_data.field_type, 
            field_id=field_data.id,
            order_by_value=order_up_or_down
        )
    # ------------------------------------------------------------------------------------------
    def _sort_user(self, order_up_or_down, field_data):
        return FormValue.data_.form_depends_on_and_values_for_sort_user_field_types(
            company_id=self.company_id, 
            depends_on_forms=self._data, 
            field_type=field_data.field_type,
            field_id=field_data.id,
            user_ids_ordered=list(UserExtended.data_.user_ids_for_sort_by_company_id(
                self.company_id,
                order_up_or_down
            ))
        )
    # ------------------------------------------------------------------------------------------
    def _sort_form(self, order_up_or_down, field_data):
        return FormValue.data_.form_depends_on_and_values_for_sort_form_field_types(
            company_id=self.company_id, 
            depends_on_forms=self._data, 
            field_id=field_data.id,
            field_type=field_data.field_type, 
            form_field_as_option_id=field_data.form_field_as_option_id,
            order_by_value=order_up_or_down,
        )
    # ------------------------------------------------------------------------------------------
    def _sort_number(self, order_up_or_down, field_data):
        # reference: https://stackoverflow.com/a/18950952/13158385
        return FormValue.data_.form_depends_on_and_values_for_sort_number_field_types(
            company_id=self.company_id, 
            depends_on_forms=self._data, 
            field_type=field_data.field_type,
            field_id=field_data.id,
            order_by_value=order_up_or_down
        )
    # ------------------------------------------------------------------------------------------
    def _sort_formula(self, order_up_or_down, field_data):
        """
        When the field type is a formula what we do is check the last field type, and order by it. 
        If the formula changed from a number to a date we will order by date, otherwise we will order by number because it was the last
        data inserted.

        Args:
            order_up_or_down (str): '-value' or 'value' check here: https://docs.djangoproject.com/en/dev/ref/models/querysets/#order-by
            field_data (reflow_server.data.services.data.data.FieldData): the FieldData object, it doesn't present anything just a dataclass
            with some handy attributes

        Returns:
            django.db.models.QuerySet(tuple(int, str)): A queryset of tuples where the first value is the main_form_id and the second is the value
        """
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

        return self.__sort(order_up_or_down, field_data)