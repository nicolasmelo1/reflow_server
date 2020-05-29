from django.conf import settings
from django.db.models import Case, When, Value, CharField, functions
from reflow_server.formulary.models import FormValue
from reflow_server.authentication.models import UserExtended


class SortItem:
    def __init__(self, field_name, value):
        self.field_name = field_name
        self.value = value
    
    @staticmethod
    def convert_sort_data(sort_data):
        sort_objects = list()
        for sort in sort_data:
            [(field_name, (field_value, search_exact))] = sort.items()
            sort_objects.append(SortItem(field_name, field_value, search_exact))
        return sort_objects


class DataSort:
    def __sort(self, sort_keys):
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
            field_data = self.__fields[to_sort.field_name]
            filter_up_or_down = 'value' if 'down' in to_sort.value else '-value'

            # tries to find a handler to sort specific field_types
            # if a handler is found or not, we return the value and the formulary_id
            # this way we can give a number to each formulary_id individually. so they can be sorted.
            handler = getattr(self, '_sort_%s' % field_data['type'], None)
            if handler:
                orderded_values_and_form_ids = handler(filter_up_or_down, field_data)
            else:
                orderded_values_and_form_ids = FormValue.objects.filter(
                        company=self.company, 
                        form__depends_on__in=self.__data, 
                        field_id=field_data['id']
                    ) \
                    .order_by(filter_up_or_down) \
                    .values('form__depends_on', 'value')
            
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
                # if we have options like `RJ` and `SP` for regions, and `Todo` and `Done` we end with 4 possible keys:
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
            if self.__data and order:
                self.__data = self.__data.order_by(order)


    def _sort_date(self, filter_up_or_down, field_data):
        return FormValue.objects.filter(
                company_id=self.company_id, 
                form__depends_on__in=self.__data, 
                field_type__type=field_data['type'], 
                field_id=field_data['id']
            ) \
            .extra(select={'date': "to_timestamp(value, '{}')".format(settings.DEFAULT_PSQL_DATE_FIELD_FORMAT)}) \
            .extra(order_by=[filter_up_or_down.replace('value', 'date')]) \
            .values('form__depends_on', 'value')
         
    def _sort_user(self, filter_up_or_down, field_data):
        filter_up_or_down = 'full_name' if filter_up_or_down == 'value' else '-full_name'
        user_id_order = UserExtended.objects.filter(
                company_id=self.company_id, 
                is_active=True
            ) \
            .annotate(
                full_name=functions.Concat('first_name', Value(' '), 'last_name', 
                output_field=CharField())
            ) \
            .order_by(filter_up_or_down) \
            .values_list('id', flat=True)
        
        order = Case(*[When(value=str(value), then=pos) for pos, value in enumerate(user_id_order)])
        return FormValue.objects.filter(
                company_id=self.company_id, 
                form__depends_on__in=self.__data, 
                field_type__type=field_data['type'],
                value__in=list(user_id_order),
                field_id=field_data['id']
            )\
            .order_by(order) \
            .values('form__depends_on', 'value')
    

    def _sort_form(self, filter_up_or_down, field_data):
        form_value_order = FormValue.objects.filter(
                company_id=self.company_id, 
                field=field_data['form_field_as_option']
            ) \
            .order_by(filter_up_or_down) \
            .values_list('form', flat=True)

        # we force a order of for each form_value that contains the form_id as the value of the field.
        order = Case(*[When(value=str(value), then=pos) for pos, value in enumerate(form_value_order)])
        return FormValue.objects.filter(
                company=self.company, 
                form__depends_on__in=self.__data, 
                field_type__type=field_data['type'], 
                value__in=list(form_value_order),
                field_id=field_data['id']
            ) \
            .order_by(order) \
            .values('form__depends_on', 'value')
