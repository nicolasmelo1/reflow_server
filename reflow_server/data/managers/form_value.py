from django.conf import settings
from django.db import models
from django.db.models import Q, Case, When, Value, CharField, FloatField, IntegerField
from django.db.models.functions import NullIf, Coalesce, Cast


class FormValueDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    # ------------------------------------------------------------------------------------------
    def create_or_update(self, field, field_type, company_id, date_configuration_date_format_type, 
                        period_configuration_period_interval_type, number_configuration_number_format_type,
                        formula_configuration, form_field_as_option, value, section, form_value_id=None):
        """
        Used for creating or updating a FormValue instance. We only return the created or updated instance, we don't
        return the True or False signaling if it was created or not

        Args:
            field (reflow_server.formulary.models.Field): The Field instance of this FormValue, this is for reference
                                                          on what field does this value references to
            field_type (reflow_server.formulary.models.FieldType): This is an state about the type of the field. 
                                                                   Field states are used to hold the 
                                                                   information on how the field was configured when we 
                                                                   saved it's value.
            company_id (reflow_server.authentication.models.Company): For what company does this value references to, we 
                                                                      save this here, so we don't need to do many joins
                                                                      to get the values
            date_configuration_date_format_type (reflow_server.formulary.models.FieldDateFormatType): 
                                                    This is an state about the `date_format_type` of the field. 
                                                    Field states are used to hold the information on how the field 
                                                    was configured when we saved it's value.
            period_configuration_period_interval_type (reflow_server.formulary.models.FieldPeriodIntervalType): 
                                                    This is an state about the `period_interval_type` of the field. 
                                                    Field states are used to hold the information on how the field 
                                                    was configured when we saved it's value.
            number_configuration_number_format_type (reflow_server.formulary.models.FieldNumberFormatType): 
                                                    This is an state about the `number_format_type` of the field. 
                                                    Field states are used to hold the information on how the field 
                                                    was configured when we saved it's value.
            formula_configuration (str): The state of the formula configured for the field when we saved it's value.
                                         We just copy the formula on the field instance to here.
            form_field_as_option (reflow_server.formulary.models.Field): This is the field to use as option on `form`
                                                                         field types. This is also an state about what field
                                                                         from what formulary the formulary id saved as value 
                                                                         references to.
            value (str): The actual value of the FormValue instance. This is always an string, but what is saved can change.
                         Sometimes it's a number, but this number references an id of a row of another table. Sometimes
                         it's a date, and so on.
            section (reflow_server.data.models.DynamicForm): This is an DynamicForm with depends_on value as NOT NULL.
            form_value_id (int, optional): If you are updating an instance You must set this, If set To false will create
                                              a new FormValue instance. Defaults to None.

        Returns:
            reflow_server.data.models.FormValue: Returns an FormValue instance, this instance represents what was saved on the
                                                 database.
        """
        instance, __ = super().get_queryset().update_or_create(id=form_value_id,
            defaults={
                'field': field,
                'field_type': field_type,
                'company_id': company_id,
                'date_configuration_date_format_type': date_configuration_date_format_type,
                'period_configuration_period_interval_type': period_configuration_period_interval_type,
                'number_configuration_number_format_type': number_configuration_number_format_type,
                'formula_configuration': formula_configuration,
                'form_field_as_option': form_field_as_option,
                'value': value,
                'form': section
            }
        )
        return instance
    # ------------------------------------------------------------------------------------------
    def form_value_id_field_name_form_field_as_option_id_number_format_id_date_format_id_field_type_value_field_id_and_form_depends_on_by_main_form_ids_company_id_and_field_ids(
        self, main_form_ids, company_id, field_ids=[]
    ):
        """
        Gets the following data
        'id'
        'field__name'
        'form_field_as_option_id'
        'number_configuration_number_format_type_id'
        'date_configuration_date_format_type_id'
        'field_type__type'
        'value'
        'field_id'
        'form__depends_on_id'
        of the FormValue instances from a list of main_form_ids (those are not section ids) and from a company_id

        Args:
            main_form_ids (list(int)): a list of DynamicForm instance ids where depends_on IS NULL.
            company_id (int): a Company instance id.
            field_ids (list[int], optional): a list of Field instance ids so we don't retrieve EVERY FormValue instance of the DynamicForm. Defaults to [].

        Returns:
            django.db.models.QuerySet(dict): Returns a queryset of dicts
        """
        order = Case(*[When(id=form_data_id, then=index) for index, form_data_id in enumerate(main_form_ids)])
        instances = self.get_queryset().filter(form__depends_on_id__in=main_form_ids, company_id=company_id).order_by(order)
        if field_ids:
            instances = instances.filter(field_id__in=field_ids)
        return instances.values(
            'id', 
            'field__name', 
            'form_field_as_option_id', 
            'number_configuration_number_format_type_id',
            'date_configuration_date_format_type_id',
            'field_type__type', 
            'value', 
            'field_id', 
            'form__depends_on_id'
        )
    # ------------------------------------------------------------------------------------------
    def form_values_by_value_field_id_and_section_id(self, value, field_id, section_id):
        """
        Gets FormValue instances by the value, field_id and section_id of this FormValue

        Args:
            value (str): from what value you want to retrieve FormValue instances from
            field_id (int): the field_id of this value
            section_id (int): from what section this field is from.

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValues based on the parameters
        """
        return self.get_queryset().filter(value=value, field_id=field_id, form__form_id=section_id)
    # ------------------------------------------------------------------------------------------
    def form_value_by_form_value_id(self, form_value_id):
        """
        Gets a single instance based on a FormValue instance id

        Args:
            form_value_id (int): the id of the form value instance

        Returns:
            reflow_server.data.models.FormValue: The FormValue instance
        """
        return self.get_queryset().filter(id=form_value_id).first()
    # ------------------------------------------------------------------------------------------
    def value_by_form_value_id(self, form_value_id):
        """
        Gets a single value based on a FormValue instance id

        Args:
            form_value_id (int): the id of the form value instance

        Returns:
            reflow_server.data.models.FormValue: The single FormValue instance
        """
        return self.get_queryset().filter(id=form_value_id).values_list('value', flat=True).first()
    # ------------------------------------------------------------------------------------------   
    def form_value_by_form_id_and_field_id(self, form_id, field_id):
        """
        Returns a single dict based on a FormValue containing the following keys: `value`, `field_type__type`, `form_field_as_option_id`

        Args:
            form_id (int): From which section_id you want to retrieve the FormValue data
            field_id (int): From which field_id you want to retrieve the FormValue data

        Returns:
            reflow_server.data.models.FormValue: A FormValue instance
        """
        return self.get_queryset().filter(form_id=form_id, field_id=field_id).first()
    # ------------------------------------------------------------------------------------------
    def value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty(self, depends_on_ids, field_type_id, field_id):
        """
        Gets a QuerySet from tuples where the first index of the tuple contains the value, and the second index is the form_id it is from.
        This form_id recieved is the main formulary id, and not the section id. 
        The queryset here doesn't comply NULL or EMPTY values.

        Args:
            depends_on_ids (list(int)): This is a list of main formulary ids and not section ids from what forms you want to retrieve this FormValues from
            field_type_id (int): The id of the FieldType of this particular field. We use this to retrieve exactly the same FieldType as the Field you are retrieving.
            field_id (int): The id of the field of the FormValue

        Returns:
            django.db.models.QuerySet(tuple): This is a queryset of tuples, used retrived from the `.values_list` function. Each tuple contains the first index as 
            the value, and the second index as the `form_id` it is from (form_id is the main formulary id, and not the section id).
        """
        return self.get_queryset().filter(
            form__depends_on_id__in=depends_on_ids, 
            field_type_id=field_type_id, 
            field_id=field_id, 
        ).exclude(
            Q(value='') | Q(value__isnull=True)
        ).values_list('value', 'form__depends_on_id')
    # ------------------------------------------------------------------------------------------
    def distinct_value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty_ordered(self, depends_on_ids, field_type_id, field_id, order=[]):
        """
        It is basically the same as `value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty` method, except it gives us
        only the distinct values.
        This query also orders by values. If you want your results to be ordered you need to send the order in `order` parameter as list.

        Args:
            depends_on_ids (list(int)): This is a list of main formulary ids and not section ids from what forms you want to retrieve this FormValues from
            field_type_id (int): The id of the FieldType of this particular field. We use this to retrieve exactly the same FieldType as the Field you are retrieving.
            field_id (int): The id of the field of the FormValue
            order (optional, list(str)): List of strings, each string is a value. The list you send is the order we will follow. Default as [].

        Returns:
            django.db.models.QuerySet(tuple): This is a queryset of tuples, used retrived from the `.values_list` function. Each tuple contains the first index as 
            the value, and the second index as the `form_id` it is from (form_id is the main formulary id, and not the section id).
        """
        data = self.value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty(depends_on_ids, field_type_id, field_id)\
                .distinct()
        if order:
            order = Case(*[When(value=str(value), then=pos) for pos, value in enumerate(order)])
            data = data.order_by(order)
        return data
    # ------------------------------------------------------------------------------------------
    def form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(self,company_id, depends_on_forms, field_ids, field_types):
        """
        Gets a queryset of FormValues based on a list of main forms, the company_id that you want to retrieve, a list of field_ids and a list 
        of field_types as string.

        Args:
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_ids (list(int)): The list of field ids to filter 
            field_types (list(str)): The list of field types to filter, it's important to notice that we filter by the state of the FormValue.
            Since FormValues are imutable we actually save the state of the value on FormValues saving the number format, the date format and also the field type.
            So here we filter only the values that are of the following state.
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValues based on the parameters
        """
        return self.get_queryset().filter(form__depends_on__in=depends_on_forms, field__in=field_ids, field_type__type__in=field_types, company_id=company_id)
    # ------------------------------------------------------------------------------------------
    def form_depends_on_ids_for_search_all_field_types(self, company_id, depends_on_forms, field_id, field_type, search_value_dict):
        """
        This is similar from the `form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id` method. But here we also filter the values
        from the `value` column. We don't filter the value directly, since the value can be an ilike or not we recieve a dict that we use as kwargs see here:
        https://docs.djangoproject.com/en/3.1/ref/models/querysets/#icontains

        This method is used for most field_types, other specific field types like `date`, `form`, `user` and etc, has it's own methods for handling search.

        So if you want to filter the value by ilike you must send the dict this way: 
        >>> {
            'value__icontains': <VALUE>
        }

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we filter by the state of the FormValue.
            search_value_dict (dict): This dict we will use as kwargs when we filter, usualy this filter in the `value` column. We filter by two conditions
            it can be an ilike or not. So this dict should be like the following:
            >>> {
                'value__icontains': <VALUE>
            }
            and:
            >>> {
                'value': <VALUE>
            }

        Returns:
            django.db.models.QuerySet(int): This is a queryset with `form__depends_on__id`s. These ids are the Main Formulary ids and not section ids.
        """
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type])\
            .filter(**search_value_dict)\
            .values_list('form__depends_on__id', flat=True)
    # ------------------------------------------------------------------------------------------
    def form_depends_on_ids_for_search_date_field_types(self, company_id, depends_on_forms, field_id, field_type, start_date, end_date):
        """
        Similar of `form_depends_on_ids_for_search_all_field_types` method but only used for `date` field types

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we filter by the state of the FormValue.
            start_date (datetime.datetime): The start date of the range to filter and search
            end_date (datetime.datetime): The end date of the range to filter and search

        Returns:
            django.db.models.QuerySet(int): This is a queryset with `form__depends_on__id`s. These ids are the Main Formulary ids and not section ids.
        """
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type])\
            .filter(value__range=(start_date, end_date))\
            .values_list('form__depends_on__id', flat=True)
    # ------------------------------------------------------------------------------------------
    def form_depends_on_ids_for_search_form_field_types(self, company_id, depends_on_forms, field_id, field_type, form_field_as_option_id, search_value_dict):
        """
        Similar of `form_depends_on_ids_for_search_all_field_types` method but only used for `form` field types. Here we make two queries.
        The first query we make is on the form_field_as_option, so on the field we use as option. Don't forget that `form` field_types actually
        hold the id of the reference in the value.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we filter by the state of the FormValue.
            form_field_as_option_id (int): The id of the Field to use as option.
            search_value_dict (dict): This dict we will use as kwargs when we filter, usualy this filter in the `value` column. We filter by two conditions
            it can be an ilike or not. So this dict should be like the following:
            >>> {
                'value__icontains': <VALUE>
            }
            and:
            >>> {
                'value': <VALUE>
            }

        Returns:
            django.db.models.QuerySet(int): This is a queryset with `form__depends_on__id`s. These ids are the Main Formulary ids and not section ids.
        """
        real_search_values = list(
            self.get_queryset().filter(
                company_id=company_id, 
                field_id=form_field_as_option_id,
                **search_value_dict
            ).values_list('form', flat=True)
        )
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type])\
            .filter(value__in=real_search_values)\
            .values_list('form__depends_on__id', flat=True)
    # ------------------------------------------------------------------------------------------
    def form_depends_on_ids_for_search_user_field_types(self, company_id, depends_on_forms, field_id, field_type, search_user_ids):
        """
        Similar of `form_depends_on_ids_for_search_all_field_types` method but only used for `user` field types

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we filter by the state of the FormValue.
            search_user_ids (list(int)): The user ids to filter, on `user` field types we actually hold the id of the user_id in the value, and not the actual value.

        Returns:
            django.db.models.QuerySet(int): This is a queryset with `form__depends_on__id`s. These ids are the Main Formulary ids and not section ids.
        """
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type])\
            .filter(value__in=search_user_ids)\
            .values_list('form__depends_on__id', flat=True)
    # ------------------------------------------------------------------------------------------
    def form_depends_on_and_values_for_sort_all_field_types(self, company_id, depends_on_forms, field_id, order_by_value):
        """
        This method is used to sort the form_depends_on and values of FormValue model for all field types. 
        We actually don't filter by any field_type, so if the field type does not match
        the field_type of the field it will be sorted anyway. Some special cases like `users` and `form`  
        It's important to notice that here we don't use the `form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id` to sort.
        This is because that this method here a` field_types needs to have
        the types of the field matched on the FormValue.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            order_by_value (enum('value', '-value')): This is the string to use in the order_by clause of the query. 
            https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
            It can be either `value` for ascending order or `-value` for descending order.

        Returns:
            django.db.models.QuerySet(tuple('form__depends_on', 'value')): This is a queryset of tuples with
            the `form__depends_on` being the first element of the tuple and the `value` being the second element of each tuple.
        """
        return self.get_queryset().filter(
            company_id=company_id, 
            form__depends_on__in=depends_on_forms, 
            field_id=field_id
        )\
        .order_by(order_by_value)\
        .values('form__depends_on', 'value')
    # ------------------------------------------------------------------------------------------
    def form_depends_on_and_values_for_sort_date_field_types(self, company_id, depends_on_forms, field_id, field_type, order_by_value):
        """
        This is similar to `form_depends_on_and_values_for_sort_all_field_types` method. Excepts that it is specifically for 
        `date` field types. It's important to notice that here we need the field_type, so if you've saved a data that was 
        of another type for this particular field we actually don't consider it in the ordering.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we order by the state of the FormValue.
            order_by_value (enum('value', '-value')): This is the string to use in the order_by clause of the query. 
            https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
            It can be either `value` for ascending order or `-value` for descending order.

        Returns:
            django.db.models.QuerySet(tuple('form__depends_on', 'value')): This is a queryset of tuples with
            the `form__depends_on` being the first element of the tuple and the `value` being the second element of each tuple.
        """
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type]) \
            .extra(select={'date': "to_timestamp(value, '{}')".format(settings.DEFAULT_PSQL_DATE_FIELD_FORMAT)}) \
            .extra(order_by=[order_by_value.replace('value', 'date')]) \
            .values('form__depends_on', 'value')
    # ------------------------------------------------------------------------------------------
    def form_depends_on_and_values_for_sort_user_field_types(self, company_id, depends_on_forms, field_id, field_type, user_ids_ordered):
        """
        This is similar to `form_depends_on_and_values_for_sort_all_field_types` method. Excepts that it is specifically for 
        `user` field types. It's important to notice that here we need the field_type, so if you've saved a data that was 
        of another type for this particular field we actually don't consider it in the ordering.

        On this case we don't use `order_by_value` parameter, instead we use `user_ids_ordered` which is a list of ordered
        user_ids that we use to order FormValue models.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we order by the state of the FormValue.
            user_ids_ordered (list(int)): This is a list of ordered user_ids we will use this list to order the form_values respecting
            the order of the ids on this list. 

        Returns:
            django.db.models.QuerySet(tuple('form__depends_on', 'value')): This is a queryset of tuples with
            the `form__depends_on` being the first element of the tuple and the `value` being the second element of each tuple.
        """
        order = Case(*[When(value=str(value), then=pos) for pos, value in enumerate(user_ids_ordered)])
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type]) \
            .filter(value__in=user_ids_ordered)\
            .order_by(order) \
            .values('form__depends_on', 'value')
    # ------------------------------------------------------------------------------------------
    def form_depends_on_and_values_for_sort_form_field_types(self, company_id, depends_on_forms, field_id, field_type, form_field_as_option_id, order_by_value):
        """
        This is similar to `form_depends_on_and_values_for_sort_all_field_types` method. Excepts that it is specifically for 
        `form` field types. It's important to notice that here we need the field_type, so if you've saved a data that was 
        of another type for this particular field we actually don't consider it in the ordering.

        On this case we use the `form_field_as_option_id` parameter, this is because we first order the values from THE field
        on this parameter and then we use the ids to filter the REAL field_id form.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we order by the state of the FormValue.
            form_field_as_option_id (int): This is similat of a field_id, except it is the form field to use as option on `form` field types
            We use this to order by this value before ordering from the recieved field_id.
            order_by_value (enum('value', '-value')): This is the string to use in the order_by clause of the query. 
            https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
            It can be either `value` for ascending order or `-value` for descending order.

        Returns:
            django.db.models.QuerySet(tuple('form__depends_on', 'value')): This is a queryset of tuples with
            the `form__depends_on` being the first element of the tuple and the `value` being the second element of each tuple.
        """
        form_value_order = self.get_queryset().filter(
                company_id=company_id, 
                field_id=form_field_as_option_id
            ) \
            .order_by(order_by_value) \
            .values_list('form', flat=True)

        # we force a order of for each form_value that contains the form_id as the value of the field.
        order = Case(*[When(value=str(value), then=pos) for pos, value in enumerate(form_value_order)])
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type]) \
            .filter(value__in=list(form_value_order)) \
            .order_by(order) \
            .values('form__depends_on', 'value')
    # ------------------------------------------------------------------------------------------
    def form_depends_on_and_values_for_sort_number_field_types(self, company_id, depends_on_forms, field_id, field_type, order_by_value):
        """
        This is similar to `form_depends_on_and_values_for_sort_all_field_types` method. Excepts that it is specifically for 
        `number` field types. It's important to notice that here we need the field_type, so if you've saved a data that was 
        of another type for this particular field we actually don't consider it in the ordering.

        To understand this query you might want to read this reference: https://stackoverflow.com/a/18950952/13158385
        Since numbers can be formulas we need to remove the #N/A or #ERROR values that can happen in formulas. And also the empty values.
        Then we need to cast the values as FLOAT so we can order it, ordering by string will put 100000 and 1 near each other.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            depends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we order by the state of the FormValue.
            order_by_value (enum('value', '-value')): This is the string to use in the order_by clause of the query. 
            https://docs.djangoproject.com/en/3.1/ref/models/querysets/#django.db.models.query.QuerySet.order_by
            It can be either `value` for ascending order or `-value` for descending order.

        Returns:
            django.db.models.QuerySet(tuple('form__depends_on', 'value')): This is a queryset of tuples with
            the `form__depends_on` being the first element of the tuple and the `value` being the second element of each tuple.
        """
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type]) \
            .annotate(value_without_na_or_error=Case(*[When(value__in=['', '#N/A', '#ERROR'], then=Value(None))], default='value', output_field=CharField())) \
            .annotate(value_as_float=Cast(Coalesce(NullIf('value_without_na_or_error', Value('')), Value('0')), FloatField())) \
            .order_by(order_by_value.replace('value', 'value_as_float')) \
            .values('form__depends_on', 'value')
    # ------------------------------------------------------------------------------------------
    def attachment_form_values_by_main_form_id_excluding_form_value_ids_and_disabled_fields(self, dynamic_form_id, form_value_ids):
        """
        Gets all FormValue instances that are from the `attachment` field_type.

        Args:
            dynamic_form_id (int): The main form_id. This is not the form_id of the section but instead of the main form data (with depends_on as None)
            form_value_ids (list(int)): A list of FormValue ids to ignore.

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValue instances based on the
                                                                            parameters
        """
        return self.get_queryset().filter(form__depends_on_id=dynamic_form_id, field_type__type='attachment')\
        .exclude(
            Q(id__in=form_value_ids) | Q(field__enabled=False) | Q(field__form__enabled=False)
        )
    # ------------------------------------------------------------------------------------------
    def delete_form_values_by_main_form_id_excluding_form_value_ids_disabled_fields_and_conditional_excludes_if_not_set(self, dynamic_form_id, form_value_ids):
        """
        Really similar to `attachment_form_values_by_main_form_id_excluding_form_value_ids_and_disabled_fields` method
        except this does not filter by attachments only, it filters FormValue instances for all field types. Then it deletes
        it. So it doesn't retrieve data, it deletes data.

        Args:
            dynamic_form_id (int): The main form_id. This is not the form_id of the section but instead of the main form data (with depends_on as None)
            form_value_ids (list(int)): A list of FormValue ids to ignore.

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValue instances based on the
                                                                            parameters
        """
        return self.get_queryset().filter(form__depends_on_id=dynamic_form_id)\
        .exclude(
            Q(id__in=form_value_ids) | Q(field__enabled=False) | Q(field__form__enabled=False) | Q(field__form__conditional_excludes_data_if_not_set=False)
        ).delete()
    # ------------------------------------------------------------------------------------------
    def last_saved_value_of_id_field_type(self, section_id, field_type_id, field_id):
        """
        Gets the biggest saved value of an id field_type, we use this to create a new when we save a new value of type `id`.
        For this we need the field_type_id, the field_id and also the section_id. This section_id is not from the data saved
        but from the formulary.

        Args:
            section_id (int): This section id is an id of a Form instance where depends_on is not NULL
            field_type_id (int): This id is the id of the `id` field_type
            field_id (int): The field id is an id of a Field instance.

        Returns:
            str: returns the biggest value saved.
        """
        return self.get_queryset().filter(
            form__form_id=section_id, 
            field_type_id=field_type_id, 
            field_id=field_id
        )\
        .annotate(value_as_int=Cast('value', IntegerField()))\
        .order_by('-value_as_int')\
        .values_list('value_as_int', flat=True)\
        .first()
    # ------------------------------------------------------------------------------------------
    def exists_form_value_by_value_field_id_and_section_id(self, value, field_id, section_id):
        """
        Verifies if a value of a field_id and of a section_id exists or not.

        Args:
            value (str): The value you want to verify if existst
            field_id (int): For what field you want to check if this value exists
            section_id (int): For what section is this field from

        Returns:
            bool: True or false if it exists or not
        """
        return self.form_values_by_value_field_id_and_section_id(value, field_id, section_id).exists()
    # ------------------------------------------------------------------------------------------
    def exists_form_value_by_value_field_id_and_section_id_excluding_form_value_id(self, value, field_id, section_id, form_value_id):
        """
        Really similar to `exists_form_value_by_value_field_id_and_section_id` method, excepts
        it doesn't consider a single form_value_id

        Args:
            value (str): The value you want to verify if existst
            field_id (int): For what field you want to check if this value exists
            section_id (int): For what section is this field from
            form_value_id (int): What form_value_id you want to exclude from this search to check if
                                 exists or not
        Returns:
            bool: True or false if it exists or not
        """
        return self.form_values_by_value_field_id_and_section_id(value, field_id, section_id).exclude(id=form_value_id).exists()
    # ------------------------------------------------------------------------------------------
    