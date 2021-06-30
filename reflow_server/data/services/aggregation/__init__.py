from django.conf import settings

from reflow_server.data.services.aggregation.data import AggregationData
from reflow_server.data.services.representation import RepresentationService
from reflow_server.data.services.data import DataService
from reflow_server.data.models import FormValue
from reflow_server.formulary.models import Field, FieldOptions
from reflow_server.formulary.services.fields import FieldService

import functools
import decimal


class AggregationService:
    """
    Why we use numpy with reduce can be explained here:
    https://stackoverflow.com/a/23982749/13158385
    """
    def __init__(self, user_id, company_id, form_id, query_params={}, search_keys=[], sort_keys=[], from_date=None, to_date=None):
        self.dynamic_form_ids_to_aggregate = DataService.get_user_form_data_ids_from_query_params(
            query_params=query_params, 
            user_id=user_id,
            company_id=company_id,
            form_id=form_id
        )
    
    def __sum_list(self, values):
        result = 0
        if len(values) > 0:
            result = functools.reduce(lambda x, y: self.__convert_to_int(x) + self.__convert_to_int(y), values)
        return result

    def __convert_to_int(self, value):
        """
        This is necessary to convert a certain value to int in a Try and Except fashion,
        we need this because sometimes we can throw an error while converting to int, especially
        in a reduce function. So this function recieves a value, and tries to convert to int
        if an error is thrown it returns as 0 instead.

        Args:
            value (any): the value to convert

        Returns:
            int: the integer converted.
        """
        try:
            return int(value)
        except ValueError as ve:
            return 0

    def __order_keys(self, field):
        """
        This is used because of a business requirement. The keys of the aggregation
        must be ordered if we are agregation by an `option` label. The same happen
        to dates.

        Args:
            field (reflow_server.formulary.models.Field): This is the field we use as key on the aggragation

        Returns:
            list(str): Returns a list of values to be ordered, the order of the items in the list is the order we use.
        """
        if field.type.type == 'option':
            return FieldOptions.objects.filter(field=field).order_by('order').values_list('option', flat=True)
        elif field.type.type == 'date':
            order_data = FormValue.data_.form_depends_on_and_values_for_sort_date_field_types(
                field.form.depends_on.group.company_id, 
                self.dynamic_form_ids_to_aggregate,
                field.id,
                field.type.type,
                'value'
            )
            return list(dict.fromkeys([to_order['value'] for to_order in order_data]))
        else:
            return []

    def aggregate(self, method, field_id_key, field_id_value, formated=False):
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

        By default this function doesn't care about formatting so all of the numbers returned by 
        default are on the default BASE defined by DEFAULT_BASE_NUMBER_FIELD_FORMAT.
        For keys on the other hand they are not formatted also so dates will follow the default
        date formating. 
        To override both the default BASE and the default Keys you must set `formated` parameter 
        to True so we convert each key to their following representations and divide each value by 
        DEFAULT_BASE_NUMBER_FIELD_FORMAT.
        
        Args:
            method (str): Use this to define the method to aggregate, check the methods with
                          `_aggregate_` keyword on this class for the possible options.
            field_id_key (int): The key to aggregate
            field_id_value (int): The field_id to use for the value.
            formated (bool, optional): if you want the key formatted set this to True
                                       so we can format the results, if this is none we don't format
                                       the values, nor keys. Defaults to False.

        Raises:
            KeyError: If the `method` does not exist it will throw an error.

        Returns:
            dict: Usually aggregation can be represented as something like this and this is what
                  we return
            >>> {
                '12/08/20': 100,
                '13/08/20': 200,
                '14/08/20': 400,
                '15/08/20': 50,
                '16/08/20': 200,
            }
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
        
        key_field_type = FieldService.retrieve_actual_field_type_for_field(key_field.id, key_field.type)
        value_field_type = FieldService.retrieve_actual_field_type_for_field(value_field.id, value_field.type)

        keys_ordering = self.__order_keys(key_field)
        keys_values = FormValue.data_.distinct_value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty_ordered(
            depends_on_ids=self.dynamic_form_ids_to_aggregate, 
            field_type_id=key_field_type.id, 
            field_id=key_field.id, 
            order=keys_ordering
        )

        for key_value, key_form_data_id in keys_values:
            aggregation_data.add_key(key=key_value, form_data_id=key_form_data_id)
        
        value_values = FormValue.data_.value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty(
            depends_on_ids=self.dynamic_form_ids_to_aggregate, 
            field_type_id=value_field_type.id, 
            field_id=value_field.id, 
        )

        for value_value, value_form_data_id in value_values:
            aggregation_data.add_value(value=value_value, form_data_id=value_form_data_id)

        aggregation_result_data = method_handler(aggregation_data.aggregated, value_field_type.type)
        formated_aggregation_result_data = {}
        if formated:
            for key, value in aggregation_result_data.items():
                key_representation = RepresentationService(
                    key_field.type.type,
                    key_field.date_configuration_date_format_type_id,
                    key_field.number_configuration_number_format_type_id,
                    key_field.form_field_as_option_id,
                    load_ids=False
                )
                value = value if type(value) in [int, float] else 0
                formated_aggregation_result_data[key_representation.representation(key)] = value/settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT
        else:
            formated_aggregation_result_data = aggregation_result_data
        return formated_aggregation_result_data

    def _aggregate_sum(self, formated_data, field_type):
        """
        ONLY WORKS with numbers, otherwise it is considered as 0.
        Aggregates the data by sum.
        """
        if field_type == 'number':
            for key, value in formated_data.items():
                result = self.__sum_list(value)
                formated_data[key] = int(result)
        else:
            for key in formated_data.keys():
                formated_data[key] = 0
        return formated_data
        
    def _aggregate_avg(self, formated_data, field_type):
        """
        ONLY WORKS with numbers, otherwise it is considered as 0.
        Average aggregation type so total of items by quantity of items.
        """
        if field_type == 'number':
            for key, value in formated_data.items():
                result = self.__sum_list(value)
                if len(value) > 0:
                    result = decimal.Decimal(result)/decimal.Decimal(len(value))
                formated_data[key] = int(result)
        else:
            for key in formated_data.keys():
                formated_data[key] = 0
        return formated_data

    def _aggregate_percent(self, formated_data, field_type):
        """
        ONLY WORKS with numbers, otherwise it is considered as 0.
        Percent aggregation is simple, it is each total of items by total.
        This means we first sum the total from all of the keys and divide each key
        by the total.
        """
        if field_type == 'number':
            total = 0
            # gets the total from each array, giving the full total
            for value in formated_data.values():
                result = self.__sum_list(value)
                total = int(total) + int(result)
            if total > 0:
                for key, value in formated_data.items():
                    result = self.__sum_list(value)
                    result = int(result)/int(total)
                    formated_data[key] = int(result*settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT*100)
                return formated_data
            else:
                return formated_data
        else:
            for key in formated_data.keys():
                formated_data[key] = 0 
            return formated_data
    
    def _aggregate_count(self, formated_data, field_type):
        """
        Works on every field type. Counts the values of each label.
        """
        for key, value in formated_data.items():
            formated_data[key] = int(decimal.Decimal(len(value)*settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT))
        return formated_data

    def _aggregate_max(self, formated_data, field_type):
        """
        ONLY WORKS with numbers, otherwise it is considered as 0.
        Retrieves the maximum value of the aggregation
        """
        if field_type == 'number':
            for key, values in formated_data.items():
                max_value = max([self.__convert_to_int(value) for value in values]) if values else 0
                formated_data[key] = max_value
        else:
            for key in formated_data.keys():
                formated_data[key] = 0
        return formated_data

    def _aggregate_min(self, formated_data, field_type):
        """
        ONLY WORKS with numbers, otherwise it is considered as 0.
        Retrieves the minimum value of the aggregation
        """
        if field_type == 'number':
            for key, values in formated_data.items():
                max_value = min([self.__convert_to_int(value) for value in values]) if values else 0
                formated_data[key] = max_value
        else:
            for key in formated_data.keys():
                formated_data[key] = 0
        return formated_data
     