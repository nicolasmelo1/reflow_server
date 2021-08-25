from django.db import models
from django.conf import settings
from django.db.models.expressions import ExpressionWrapper

from reflow_server.authentication.models import UserExtended
from reflow_server.filter.models import FilterCondition, FilterConditionalType, FilterConectorType
from reflow_server.data.models import FormValue

from datetime import datetime


class FilterConditionData:
    def __init__(self, field, field_type, conditional, is_negation, value, value2='', connector=None): 
        self.conditional = conditional
        self.is_negation = is_negation
        self.field = field
        self.field_type = field_type
        self.value = self.format_value(value)
        self.value2 = self.format_value(value2)
        self.connector = connector
    
    def format_value(self, value):
        if self.field.type.type == 'date':
            return datetime.strptime(value, settings.DEFAULT_DATE_FIELD_FORMAT)
        else:
            return value

class FilterDataService:
    def __init__(self, company_id, form_data_ids_to_filter=[]):
        """
        This is service responsible for filtering data. This is basically all that does. It is not supposed 
        to do anything else. The idea of filtering is to support many types of data filtering so users can save
        their filters and do stuff with it. This is used when retrieving the data for the user in the listing, 
        dashboard or kanban visualization, which are one of the most obvious ways to filter data BUT this
        can also be used for enabling user permissions, notifications and others.

        Args:
            form_data_ids_to_filter (list, optional): The DynamicForm instance ids to filter, those are the ones
                                                      that have depends_on as None. Defaults to [].
        """
        self.company_id = company_id
        self.form_data_ids_to_filter = form_data_ids_to_filter

        # format data first
        filter_conditional_types = FilterConditionalType.objects.all()
        filter_conector_types = FilterConectorType.objects.all()
        
        self.filter_conector_type_reference = {}
        self.filter_conditional_type_reference = {}
        
        for filter_conditional_type in filter_conditional_types:
            self.filter_conditional_type_reference[filter_conditional_type.id] = filter_conditional_type.name
        
        for filter_conector_type in filter_conector_types:
            self.filter_conector_type_reference[filter_conditional_type.id] = filter_conector_type.name
    
    
    def filter_condition_data_by_filter_id(self, filter_id):
        conditions = FilterCondition.objects.filter(id=filter_id)
        conditions_data = []
        
        for condition in conditions:
            if (
                (condition.conditional_type and not self.filter_conditional_type_reference.get(condition.conditional_type, None)) \
                or (condition.conector_type and not self.filter_conector_type_reference.get(condition.conector_type, None))
            ):
                raise AssertionError(
                    'Looks like the conditional or the connector you are trying to use for this does not exist'
                )

            conditions_data.append(
                FilterConditionData(
                    condition.field.id, 
                    condition.field.type.type,
                    self.filter_conditional_type_reference[condition.conditional_type], 
                    condition.value, 
                    condition.value2,
                    self.filter_conector_type_reference[condition.conector_type]
                )
            )
        return conditions_data


    def __filter_types(self, condition):
        if 'contains' in condition.conditional:
            return models.Q(
                field_id=condition.field.id,
                value2__icontains=condition.value
            )
        elif 'between' in condition.conditional:
            return models.Q(
                field_id=condition.field.id, 
                value2__range=[condition.value, condition.value2]
            )
        elif 'greater_than' in condition.conditional:
            return models.Q(
                field_id=condition.field.id,
                value2__gt=condition.value
            )
        elif 'less_than' in condition.conditional:
            return models.Q(
                field_id=condition.field.id,
                value2__lt=condition.value
            )
        elif 'greater_than_equal' in condition.conditional:
            return models.Q(
                field_id=condition.field.id,
                value2__gte=condition.value
            )
        elif 'less_than_equal' in condition.conditional:
            return models.Q(
                field_id=condition.field.id,
                value2__lte=condition.value
            )
        elif 'is_empty' in condition.conditional:
            return models.Q(
                field_id=condition.field.id,
                value2__in=[None, '']
            )
        else:
            return models.Q(
                field_id=condition.field.id, 
                value2=condition.value
            )

    def __anotation(self, condition):
        handler = getattr(self, '_anotate_%s' % condition.field_type, None)
        if handler:
            return handler(condition)
        else:
            return models.F('value')

    def _anotate_date(self, condition):
        return models.Case(
            models.When(
                field_type__type='date', 
                then=ExpressionWrapper(
                        models.Func(
                        models.F('value'),
                        models.Value(settings.DEFAULT_PSQL_DATE_FIELD_FORMAT), 
                        function='to_timestamp'
                    ),
                    output_field=models.DateTimeField()
                )
            )
        )
        
    def _anotate_number(self, condition):
        # reference: https://stackoverflow.com/a/1154977
        q = models.Q()
        q.add(models.Q(field_type__type='date'))
        q.add(~models.Q(value__in=['#N/A, #ERROR']))
        return models.Case(
            models.When(
                condition=q, 
                then=models.functions.comparison.Cast('value', output_field=models.IntegerField())
            )
        )
    
    def _anotate_form(self, condition):
        if condition.field.form_field_as_option_id:
            when_clauses = []
            # retrieves all of the FormValue instances containing only the ids of the `form` field_type it refers to.
            # in other words, this is the actual value we store in the database for the field.
            form_field_type_values = FormValue.filter_.values_of_form_field_type_by_field_id_and_field_type_id(
                condition.field.id,
                condition.field.type.id
            )
            # this is the value it refers to, the actual value you will be filtering
            form_values = FormValue.filter_.main_form_id_section_id_and_value_by_field_id_and_form_data_ids_or_section_data_ids(
                condition.field.form_field_as_option_id,
                form_field_type_values
            )
            
            for form_value in form_values:
                when_clauses.append(
                    models.When(
                        condition=models.Q(value=str(form_value['form_id'])), 
                        then=models.Value(form_value['value'], output_field=models.TextField())
                    )
                )
            return models.Case(*when_clauses)
        else:
            return models.F('value')

    def _anotate_user(self, condition):
        users_of_company = UserExtended.objects.filter(company_id=self.company_id).values('id', 'first_name', 'last_name')
        when_clauses = []

        for user_of_company in users_of_company:
            when_clauses.append(
                models.When(
                    condition=models.Q(value=str(user_of_company['id'])),
                    then=models.Value(
                        '{} {}'.format(user_of_company['first_name'], user_of_company['last_name']), 
                        output_field=models.TextField()
                    )
                )
            )
        return models.Case(*when_clauses)

    def _anotate_formula(self, condition):
        latest_form_value = FormValue.filter_.latest_form_value_field_type_by_field_id(condition.field.id)
        if latest_form_value:
            condition.field = latest_form_value.field
            condition.field_type = latest_form_value.field_type.type
            return self.__anotation(condition)
        else:
            return models.F('value')

    def search(self, condition_data):
        main_form_data_ids_to_filter = self.form_data_ids_to_filter
        main_form_data_ids_to_consider = []
        # Reference https://stackoverflow.com/a/50775442
        for condition in enumerate(condition_data):
            conditional = self.__filter_types(condition)
            annotation = self.__anotation(condition)

            form_value = FormValue.objects

            if annotation:
                form_value = form_value.annotate(value2=annotation)

            form_value = form_value.filter(form__depends_on_id__in=main_form_data_ids_to_filter).filter(conditional)
            
            # the idea is simple, if it's a 'or' we append those ids, otherwise we use only the
            # ids retrieved filtering it.
            main_form_ids = form_value.values_list('form__depends_on__id', flat=True)
            if condition.connector == 'or':
                main_form_data_ids_to_consider.append(main_form_ids)
            else:
                main_form_data_ids_to_filter = main_form_ids
                main_form_data_ids_to_consider = main_form_data_ids_to_filter
        return main_form_data_ids_to_consider
