from django.db import models
from django.conf import settings
from django.db.models.expressions import ExpressionWrapper

from reflow_server.authentication.models import UserExtended
from reflow_server.filter.models import FilterCondition, FilterConditionalType, FilterConectorType
from reflow_server.data.models import FormValue
from reflow_server.filter.services.data import FilterConditionData


class FilterDataService:
    def __init__(self, company_id):
        """
        This is service responsible for filtering data. This is basically all that does. It is not supposed 
        to do anything else. The idea of filtering is to support many types of data filtering so users can save
        their filters and do stuff with it. This is used when retrieving the data for the user in the listing, 
        dashboard or kanban visualization, which are one of the most obvious ways to filter data BUT this
        can also be used for enabling user permissions, notifications and others.

        Also this is used for the conditions on a single record/data. Like for example conditional sections. This way
        we can verify if a condition should be open or not.

        Args:
            company_id (int): A Company instance id.
        """
        self.company_id = company_id

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
        """
        By a Filter instance id we create a FilterConditionData that we can use for searching or validating the data on.

        Args:
            filter_id (int): A Filter instance id

        Raises:
            AssertionError: The conditional or connector does not exist.

        Returns:
            list(FilterConditionData): A list of FilterConditionData objects that will be used for searching or filtering.
        """
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

    def __filter_types_for_validate(self, condition, formulary_data_data):
        """
        Handles each type of filtering for the 'validate' method. If you don't know what '.validate()' is
        or does you might want to check this method before returning here.

        The idea is that this is supposed for handling each type of conditional comparison for a single record/data.
        For that we need to use the FilterFormularyDataData object. This object has the formulary_values dict
        which holds all of the fields as a dict and each key is a list of values.

        So in order to validate, as you might already know, we need to check if each value matches a particular condition.
        Beware i said "each" so we need to loop through each item in the list of values for the particular field_name.

        The most difficult part here might be the lambda function when calling the `handle_comparison`. In JS this is something very
        well known and used called a 'callback'. The idea is to validate the logic we call a function defined outside of `handle_comparison`
        function. We define this function directly when calling handle_comparison using lambda.

        This:
        >>> if condition.conditional == 'equals':
                return handle_comparison(lambda formulary_field_value: condition.value == formulary_field_value)

        could be written as:
        >>> if condition.conditional == 'equals':
                def handle_equals(formulary_field_value):
                    return condition.value == formulary_field_value
                return handle_comparison(handle_equals)

        Notice that we are passing a function to a function. We do something similar in the functionmethod decorator in the formulas but it is lot more complex.

        Args:
            condition (FilterConditionData): the FilterConditionData object that contains all of the data needed for the filtering.
            formulary_data_data (FilterFormularyDataData): A FilterFormularyDataData object with the actual data of the record/data to 
                                                           validate the conditionals to.

        Returns:
            bool: Returns true or false weather the condition is true or false
        """
        def handle_comparison(condition_logic_callback):
            if formulary_data_data.formulary_values.get(condition.field.name, None):
                for formulary_field_value in formulary_data_data.formulary_values[condition.field.name]:
                    if condition_logic_callback(formulary_field_value):
                        return not condition.is_negation
            return condition.is_negation

        if condition.conditional == 'equals':
            return handle_comparison(lambda formulary_field_value: condition.value == formulary_field_value)
        if condition.conditional == 'contains':
            return handle_comparison(lambda formulary_field_value: condition.value in formulary_field_value)
        elif condition.conditional == 'between':
            return handle_comparison(lambda formulary_field_value: condition.value <= formulary_field_value <= condition.value2)
        elif condition.conditional == 'greater_than':
            return handle_comparison(lambda formulary_field_value: condition.value > formulary_field_value)
        elif condition.conditional == 'less_than':
            return handle_comparison(lambda formulary_field_value: condition.value < formulary_field_value)
        elif condition.conditional == 'greater_than_equals':
            return handle_comparison(lambda formulary_field_value: condition.value >= formulary_field_value)
        elif condition.conditional == 'less_than_equals':
            return handle_comparison(lambda formulary_field_value: condition.value <= formulary_field_value)
        elif condition.conditional == 'is_empty':
            if formulary_data_data.formulary_values.get(condition.field.name, None) == None:
                return not condition.is_negation
            else:
                return handle_comparison(lambda formulary_field_value: formulary_field_value in ['', None])
        return condition.is_negation


    def __filter_types_for_search(self, condition, main_form_data_ids_to_filter):
        """
        As the name suggests this is responsible for handling every filter type for the 'search'.
        If you don't know what `.search()` does you might want to read the method documentation before coming here.

        This basically creates a query to add in the django ORM .filter() clause.

        Args:
            condition (FilterConditionData): the FilterConditionData object that contains all of the data needed for the filtering.
            main_form_data_ids_to_filter (list(int)): This is all of the main_form_data_ids (or DynamicForm instance ids with depends_on = None)
                                                      that we are using in our search. This is needed only for the 'is_empty' clause if the 
                                                      field_id doesn't exist for a particular dynamic_form instance.

        Returns:
            django.db.models.Q: A Q object for using in the `.filter()` clause of django ORM. 
        """
        def handle_filter_query(query):
            return models.Q(field_id=condition.field.id, **query)

        if condition.conditional == 'equals':
            return handle_filter_query({
                'value2': condition.value
            })
        elif condition.conditional == 'contains':
            return handle_filter_query({
                'value2__icontains': condition.value
            })
        elif condition.conditional == 'between':
            return handle_filter_query({
                'value2__range': [condition.value, condition.value2]
            })
        elif condition.conditional == 'greater_than':
            return handle_filter_query({
                'value2__gt': condition.value
            })
        elif condition.conditional == 'less_than':
            return handle_filter_query({
                'value2__lt': condition.value
            })
        elif condition.conditional == 'greater_than_equal':
            return handle_filter_query({
                'value2__gte': condition.value
            })
        elif condition.conditional == 'less_than_equal':
            return handle_filter_query({
                'value2__lte': condition.value
            })
        elif condition.conditional == 'is_empty':
            # we retrieve not only the form records/data when the field is empty or None but also the ones where
            # the field doesn't exist at all
            main_form_data_ids_to_exclude = FormValue.filter_.distinct_main_form_ids_by_field_id(
                condition.field.id
            )

            main_form_data_ids_where_field_id_does_not_exist = FormValue.filter_.distinct_main_form_ids_excluding_main_form_data_ids_by_main_form_data_ids(
                main_form_data_ids_to_exclude,
                main_form_data_ids_to_filter
            )
            return models.Q(
                handle_filter_query({
                    'value2__isnull': True
                }) |
                handle_filter_query({
                    'value2': ''
                }) |
                models.Q(
                    form__depends_on_id__in=main_form_data_ids_where_field_id_does_not_exist
                )
            )
        else:
            return models.Q(
                field_id=condition.field.id,
                value2=condition.value
            )

    def __anotation(self, condition):
        """
        Before doing this FilterDataService we were casting directly in the filter and it was bad because the .filter() function became so bloated and
        with so much thing that this was difficult to debug and know what was happening. Here we are doing differently we change the data using Case Where
        statements. This way we can modify the values to be the ones that we use for filtering and keep the actual filter conditional sleek and simple.

        Args:
            condition (FilterConditionData): the FilterConditionData object that contains all of the data needed for the condition.
        
        Retuns:
            (django.db.models.Case | django.db.models.F): Returns a F object with the 'value' column or a Case When clause.
        """
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
        """
        Creates an anotation on how we will handle formula fields.
        The idea is simple here, since we evaluate dynamically the formula field we retrieve the last value inserted
        and then retrieve it's type, with it we change directly the condition object recieved with the actual type
        that will be used to filter, and then 

        Args:
            condition (FilterConditionData): The FilterConditionData instance of the filter condition with it's field
                                             it's type and so on.

        Returns:
            (django.db.models.Case | django.db.models.F): Returns a F object with the name of the column to use or
                                                          a Case When clause.
        """
        latest_form_value = FormValue.filter_.latest_form_value_field_type_by_field_id(condition.field.id)
        if latest_form_value:
            condition.field = latest_form_value.field
            condition.field_type = latest_form_value.field_type.type
            return self.__anotation(condition)
        else:
            return models.F('value')

    def search(self, conditions_data, form_data_ids_to_filter=[]):
        """
        This is used to filter a conjunction of data. So it's not supposed to filter just one record/data but a conjunction of them.
        It really works like a filter of data. 

        In simple worlds this is just a query mangling we mangle many stuff about django queries here. Using specially stuff 
        like 
        - Q() #reference: https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q
        - F() #reference: https://docs.djangoproject.com/en/3.2/ref/models/expressions/#f-expressions
        - Case() When() #reference: https://docs.djangoproject.com/en/3.2/ref/models/conditional-expressions/#

        and so on.

        Just so it's easier to consume what this does, Q is for doing a query by itself, so instead of doing stuff like
        filter(name_of_the_field='value') we can add this to a Q object so we just pass the Q object to the filter like

        >>> q = Q(name_of_the_field='value')
        # and then
        .filter(q)

        The F() is for retrieving database columns, like F('value') represents the 'value' column.

        Case When there is no explanation, this is just basic SQL and the documentation explains it clearly.

        ExpressionWrapper is for running a database function and casting to a specific field type. Func() is for
        running a function specific of the databse like to_timestamp or to_string and so on. You can check the possible 
        functions in the postgres documentation. Last but not least the Value is for transforming a python value to a value
        the database can understand.


        Okay, now that i explained how to read the code let's explain what this is doing:
        - We have two lists: main_form_data_ids_to_filter and main_form_data_ids_to_consider. The first is what we will use to
        filter the data. For example, when we make a 'AND' operation we narrow the filter for each pass. The second list is
        the actual response of this function. Why do we need both? because of the 'or' operation, 'or' doesn't narrow down the search
        so we need to keep `main_form_data_ids_to_filter` untouched for each pass.
        - We loop through each FilterConditionData object to narrow down the filter for each pass or not.
        - First we get the condition we will use in the .filter() or .exclude() functions of the query for that we use Q object.
        - Second we get the anotation of the field, this way we can filter simply this is just use to convert the data to a type
        the actual database/query can understand
        - If it's a negation we append the condition to exclude otherwise append the condition to filter
        - Last but not least get the ids of the data filtered. Then we do stuff based on the connection if it's a 'or' or if 
        it's an 'and'.

        Args:
            conditions_data (list(FilterConditionData)): A list of FilterConditionData instances that we use to filter.
            form_data_ids_to_filter (list, optional): The DynamicForm instance ids to filter, those are the ones
                                                      that have depends_on as None. Defaults to [].

        Returns:
            list(int): Returns a list of distinct main_form_data_ids. So, DynamicForm instance ids where depends_on is None.
        """
        main_form_data_ids_to_filter = form_data_ids_to_filter
        main_form_data_ids_to_consider = []
        # Reference https://stackoverflow.com/a/50775442
        for condition in conditions_data:
            conditional = self.__filter_types_for_search(condition, main_form_data_ids_to_filter)
            annotation = self.__anotation(condition)

            form_value = FormValue.filter_.get_queryset()

            if annotation:
                form_value = form_value.annotate(value2=annotation)

            form_value = form_value.filter(form__depends_on_id__in=main_form_data_ids_to_filter)

            if condition.is_negation:
                form_value = form_value.exclude(conditional)
            else:
                form_value = form_value.filter(conditional)
            
            # the idea is simple, if it's a 'or' we append those ids, otherwise we use only the
            # ids retrieved filtering it.
            main_form_ids = form_value.values_list('form__depends_on__id', flat=True).distinct()
            if condition.connector == 'or':
                main_form_data_ids_to_consider.extend(list(main_form_ids))
            else:
                main_form_data_ids_to_filter = main_form_ids
                main_form_data_ids_to_consider = list(main_form_data_ids_to_filter)
        return main_form_data_ids_to_consider

    def validate(self, conditions_data, formulary_data_data):
        """
        Validates a set of conditions for a specific data/record. While search works for a group of records/data
        the validate works for a single and only record. Also the return changes, while on 'search' we return the
        DynamicForm instance ids that matches the specific set of conditions here we only return True or False.
        True means that the set of conditions passes and is valid and False if the set of conditions does not pass
        for the specific record.

        Args:
            conditions_data (list(FilterConditionData)): A list of FilterConditionData instances that we use to validate.
            formulary_data_data (FilterFormularyDataData): A FilterFormularyDataData class that is used to hold all of the data
                                                           of each field for a particular field.

        Returns:
            bool: Returns True if the set of conditionals is valid for this particular formulary data or False if it's invalid.
        """
        result = None
        for condition_data in conditions_data:
            result_of_conditional_evaluation = self.__filter_types_for_validate(condition_data, formulary_data_data)
            
            if result == None:
                result = result_of_conditional_evaluation
            else:
                if condition_data.connector == 'or':
                    result = result_of_conditional_evaluation or result
                else:
                    result = result_of_conditional_evaluation and result
        
        return result
