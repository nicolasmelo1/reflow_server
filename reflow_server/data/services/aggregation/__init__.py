from django.conf import settings
from django.db.models import Case, When, Q

from reflow_server.data.services.aggregation.data import AggregationData
from reflow_server.data.services import DataService
from reflow_server.data.models import FormValue
from reflow_server.formulary.models import Field

import numpy
import functools


class AggregationService:
    def __init__(self, user_id, company_id, form_id, search_keys=[], sort_keys=[], from_date=None, to_date=None):
        self.dynamic_form_ids_to_aggregate = DataService(
            user_id=user_id, 
            company_id=company_id
        ).get_user_form_data_ids_from_form_id(
            form_id, 
            search_keys=search_keys, 
            sort_keys=sort_keys, 
            from_date=from_date, 
            to_date=to_date
        )
        self.order = Case(*[When(id=form_data_id, then=index) for index, form_data_id in enumerate(self.dynamic_form_ids_to_aggregate)])

    def __convert_to_int(self, value):
        try:
            return int(value)
        except ValueError as ve:
            return 0

    def aggregate(self, method, field_id_key, field_id_value, field_number_format_type_id=None):
        """
        Usually aggregation can be represented something like this
        >>> {
            '12/08/20': 100,
            '13/08/20': 200,
            '14/08/20': 400,
            '15/08/20': 50,
            '16/08/20': 200,
        }

        In this case field_id_key is each key in our dict and the field_id_value is the
        field_id to aggregate by each key.

        Args:
            field_id_key (int): The key to aggregate
            field_id_value (int): The field_id to use the value.
        """
        method_handler = getattr(self, '_aggregate_%s' % method, None)
        if not method_handler:
            method_options = list()
            for key in self.__class__.__dict__.keys():
                if '_aggregate_' in key:
                    method_options.append("'%s'" % key.replace('_aggregate_', ''))
            method_options = ', '.join(method_options)
            raise KeyError("Method not valid, please use one of the following: {}".format(method_options))
        
        # this dict does not holds the result, it holds each form_id as key 
        aggregation_data = AggregationData()
        key_field = Field.objects.filter(id=field_id_key).first()
        value_field = Field.objects.filter(id=field_id_value).first()
        
        keys_values = FormValue.objects.filter(
            form__depends_on_id__in=self.dynamic_form_ids_to_aggregate, 
            field_type_id=key_field.type.id, 
            field_id=key_field.id, 
        ).exclude(
            Q(value='') | Q(value__isnull=True)
        ).values_list('value', 'form__depends_on_id').distinct()

        for key_value, key_form_data_id in keys_values:
            aggregation_data.add_key(key=key_value, form_data_id=key_form_data_id)

        value_values = FormValue.objects.filter(
            form__depends_on_id__in=self.dynamic_form_ids_to_aggregate, 
            field_type=value_field.type, 
            field_id=value_field.id, 
        ).exclude(
            Q(value='') | Q(value__isnull=True)
        ).values_list('value', 'form__depends_on_id')

        for value_value, value_form_data_id in value_values:
            aggregation_data.add_value(value=value_value, form_data_id=value_form_data_id)

        formated_data = aggregation_data.aggregated
        return method_handler(formated_data)

    def _aggregate_sum(self, formatted_data):
        for key, value in formatted_data.items():
            result = 0
            if len(value) > 0:
                value = numpy.asarray(value)
                result = functools.reduce(lambda x, y: self.__convert_to_int(x) + self.__convert_to_int(y), value)
            formatted_data[key] = int(result)/settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT
        return formatted_data
        
    def _aggregate_avg(self):
        pass