from django.conf import settings
from django.db import models
from django.db.models import Q, Sum, Case, When, Value, CharField, FloatField
from django.db.models.functions import NullIf, Coalesce, Concat, Cast


class AttachmentsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def company_aggregated_file_sizes(self, company_id):
        """
        This method calculates the aggregated file size of the attachments for a single company_id

        Args:
            company_id (int): The id of he company you want to aggregate the attachments.

        Returns:
            int: The aggregated file size
        """
        return self.get_queryset().filter(form__company_id=company_id).aggregate(Sum('file_size')).get('file_size__sum', 0)
    
    def attachment_by_dynamic_form_id_field_id_and_file_name(self, dynamic_form_id, field_id, file_name):
        """
        This retrieves a single attachment based on the dynamic_form_id, field_id and the file_name.
        It is important to notice that `dynamic_form_id` parameter can be the a section_id or a formulary_id.

        Args:
            dynamic_form_id (int): This dynamic_form_id is the id of a section or a formulary.
            field_id (int): The field id of this attachment.
            file_name (str): The file_name of the attachment.

        Returns:
            reflow_server.data.models.Attachment: Retrieves a single attachment based on the parameters recieved. 
        """
        return self.get_queryset().filter(Q(form__depends_on_id=dynamic_form_id) | Q(form_id=dynamic_form_id))\
            .filter(field_id=field_id, file=file_name).first()


class FormValueManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def form_values_by_company_id_and_form_ids(self, company_id, form_ids):
        """
        Gets form values based on the company_id and the form_ids it is from. 
        form_ids in this case are section_ids of the DynamicForm. So DynamicForm where where depends_on is not None.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            form_ids (list(int)): From which section_ids you want to retrieve the FormValues

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValues based on the parameters
        """
        return self.get_queryset().filter(company_id=company_id, form_id__in=form_ids)
    
    def form_values_by_company_id_and_form_ids_and_field_ids_ordered(self, company_id, form_ids, field_ids):
        """
        Gets a queryset of FormValues ORDERED by the field_ids. So, for every field_id it recieves in a list, it orders them.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            form_ids (list(int)): From which section_ids you want to retrieve the FormValues
            field_ids (list(int)): This list are two things, first and most important is the field_ids of the FormValues to filter, and
            second it is the how you want to order the queryset.

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A ordered queryset of FormValues based on the parameters recieved
        """
        order = Case(*[When(field_id=value, then=pos) for pos, value in enumerate(field_ids)])
        return self.form_values_by_company_id_and_form_ids(company_id, form_ids).filter(field_id__in=field_ids).order_by(order)
    
    def value_field_type_and_form_field_as_option_id_by_form_id_and_field_id(self, form_id, field_id):
        """
        Returns a single dict based on a FormValue containing the following keys: `value`, `field_type__type`, `form_field_as_option_id`

        Args:
            form_id (int): From which section_id you want to retrieve the FormValue data
            field_id (int): From which field_id you want to retrieve the FormValue data

        Returns:
            dict: This data is based on a FormValue, the dict will contain the keys: `value`, `field_type__type`, `form_field_as_option_id`
        """
        return self.get_queryset().filter(form_id=form_id, field_id=field_id).values('value', 'field_type__type', 'form_field_as_option_id').first()

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

    def distinct_value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty(self, depends_on_ids, field_type_id, field_id):
        """
        It is basically the same as `value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty` method, except it gives us
        only the distinct values

        Args:
            depends_on_ids (list(int)): This is a list of main formulary ids and not section ids from what forms you want to retrieve this FormValues from
            field_type_id (int): The id of the FieldType of this particular field. We use this to retrieve exactly the same FieldType as the Field you are retrieving.
            field_id (int): The id of the field of the FormValue

        Returns:
            django.db.models.QuerySet(tuple): This is a queryset of tuples, used retrived from the `.values_list` function. Each tuple contains the first index as 
            the value, and the second index as the `form_id` it is from (form_id is the main formulary id, and not the section id).
        """
        return self.value_and_form_depends_on_id_by_depends_on_ids_field_type_id_and_field_id_excluding_null_and_empty(depends_on_ids, field_type_id, field_id).distinct()
    
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
            epends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
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

    def form_depends_on_ids_for_search_date_field_types(self, company_id, depends_on_forms, field_id, field_type, start_date, end_date):
        """
        Similar of `form_depends_on_ids_for_search_all_field_types` method but only used for `date` field types

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            epends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
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
    
    def form_depends_on_ids_for_search_form_field_types(self, company_id, depends_on_forms, field_id, field_type, form_field_as_option_id, search_value_dict):
        """
        Similar of `form_depends_on_ids_for_search_all_field_types` method but only used for `form` field types. Here we make two queries.
        The first query we make is on the form_field_as_option, so on the field we use as option. Don't forget that `form` field_types actually
        hold the id of the reference in the value.

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            epends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
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
    
    def form_depends_on_ids_for_search_user_field_types(self, company_id, depends_on_forms, field_id, field_type, search_user_ids):
        """
        Similar of `form_depends_on_ids_for_search_all_field_types` method but only used for `user` field types

        Args:
            company_id (int): The company id from where you want to retrieve the FormValue. We use this to affunilate the search
            and to prevent any errors from retrieving FormValues of another company.
            epends_on_forms (list(reflow_server.data.models.DynamicForm)): This is a list of dynamic forms to filter it's values.
            field_id (int): On what field id you want to filter
            field_type (str): The name of field type to filter, it's important to notice that we filter by the state of the FormValue.
            search_user_ids (list(int)): The user ids to filter, on `user` field types we actually hold the id of the user_id in the value, and not the actual value.

        Returns:
            django.db.models.QuerySet(int): This is a queryset with `form__depends_on__id`s. These ids are the Main Formulary ids and not section ids.
        """
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type])\
            .filter(value__in=search_user_ids)\
            .values_list('form__depends_on__id', flat=True)

    def form_depends_on_and_values_sort_all_field_types(self, company_id, depends_on_forms, field_id, order_by_value):
        return self.get_queryset().filter(
            company_id=company_id, 
            form__depends_on__in=depends_on_forms, 
            field_id=field_id
        )\
        .order_by(order_by_value)\
        .values('form__depends_on', 'value')

    def form_depends_on_and_values_sort_date_field_types(self, company_id, depends_on_forms, field_id, field_type, order_by_value):
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type]) \
            .extra(select={'date': "to_timestamp(value, '{}')".format(settings.DEFAULT_PSQL_DATE_FIELD_FORMAT)}) \
            .extra(order_by=[order_by_value.replace('value', 'date')]) \
            .values('form__depends_on', 'value')
    
    def form_depends_on_and_values_sort_user_field_types(self, company_id, depends_on_forms, field_id, field_type, user_ids_ordered):
        order = Case(*[When(value=str(value), then=pos) for pos, value in enumerate(user_ids_ordered)])
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type]) \
            .filter(value__in=user_ids_ordered)\
            .order_by(order) \
            .values('form__depends_on', 'value')

    def form_depends_on_and_values_sort_form_field_types(self, company_id, depends_on_forms, field_id, field_type, form_field_as_option_id, order_by_value):
        form_value_order = self.get_queryset().filter(
                company_id=self.company_id, 
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

    def form_depends_on_and_values_sort_number_field_types(self, company_id, depends_on_forms, field_id, field_type, order_by_value):
        # reference: https://stackoverflow.com/a/18950952/13158385
        return self.form_values_by_depends_on_forms_field_ids_field_type_types_and_company_id(company_id, depends_on_forms, [field_id], [field_type]) \
            .annotate(value_without_na_or_error=Case(*[When(value__in=['', '#N/A', '#ERROR'], then=Value(None))], default='value', output_field=CharField())) \
            .annotate(value_as_float=Cast(Coalesce(NullIf('value_without_na_or_error', Value('')), Value('0')), FloatField())) \
            .order_by(order_by_value.replace('value', 'value_as_float')) \
            .values('form__depends_on', 'value')