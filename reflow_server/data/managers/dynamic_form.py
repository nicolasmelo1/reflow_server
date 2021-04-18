from django.db import models
from django.db.models import Q, Case, When

from datetime import datetime


class DynamicFormDataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_or_update_main_form_instance(self, form_id, user_id, company_id, main_form_instance_id=None):
        """
        Creates or updates a main DynamicForm instance. This instance is the one that have depends_on as NULL.

        Args:
            form_id (int): The Form instance id that have depends_on as NULL
            user_id (int): The UserExtended instance id of the user that is saving this data 
            company_id (int): The Company instance id, is the company that this data is from.
            main_form_instance_id (int, optional): If you are UPDATING an instance
            it must be defined. This is an DynamicForm instance id. Defaults to None.

        Returns:
            reflow_server.data.models.DynamicForm: This is the saved or updated DynamicForm instance
        """
        instance, __ = super().get_queryset().update_or_create(
            id=main_form_instance_id,
            defaults={
                'updated_at': datetime.now(),
                'form_id': form_id,
                'user_id': user_id,
                'company_id': company_id
            }
        )

        return instance

    def create_or_update_section_instance(self, section_id, user_id, company_id, main_form_instance, section_instance_id=None):
        """
        Creates or updates a section DynamicForm instance. This instance is the one that have depends_on defined so it
        needs to become after the `create_or_update_main_form_instance` method

        Args:
            form_id (int): The Form instance id that have depends_on as NOT NULL
            user_id (int): The UserExtended instance id of the user that is saving this data 
            company_id (int): The Company instance id, is the company that this data is from.
            main_form_instance (reflow_server.data.models.DynamicForm): This is the DynamicForm 
            instance that goes on the depends_on column.
            section_instance_id (int, optional): If you are UPDATING an instance
            it must be defined. This is an DynamicForm instance id. Defaults to None.

        Returns:
            reflow_server.data.models.DynamicForm: This is the saved or updated DynamicForm instance
        """
        instance, __ = super().get_queryset().update_or_create(
            id=section_instance_id, 
            defaults={
                'form_id': section_id,
                'user_id': user_id,
                'company_id': company_id,
                'depends_on': main_form_instance
            }
        )

        return instance

    def dynamic_form_by_dynamic_form_id_and_company_id(self, dynamic_form_id, company_id, form_name):
        """
        This gets a DynamicForm instance by a dynamic_form_id and a company_id.
        It's important to understand that this works for both sections (instances with depends_on as NOT NULL)
        and main forms (intances with depends_on as NULL).

        Args:
            dynamic_form_id (int): The dynamic_form_id, can be a section instance
                                   or a form instance.
            company_id (int): The id of Company instance
            form_name (str): The form name of whose form this data is from.

        Returns:
            reflow_server.data.models.DynamicForm: The DynamicForm instance.
        """
        return self.get_queryset().filter(
                Q(id=dynamic_form_id, form__group__company_id=company_id, form__form_name=form_name) | 
                Q(id=dynamic_form_id, form__depends_on__group__company_id=company_id, form__depends_on__form_name=form_name)
        ).first()
    
    def dynamic_forms_by_company_id_and_form_id_orderd_by_updated_at(self, company_id, form_id):
        """
        Gets a queryset of DynamicForm instances based on company_id and form_id ordered by `updated_at`

        Args:
            company_id (int): This is a Company instance id.
            form_id (int): A reflow_server.formulary.models.Form instance id to filter
                           the DynamicForm
        
        Returns:
            django.db.models.QuerySet(reflow_server.data.models.DynamicForm): A queryset
            of ordered DynamicForm instances by `updated_at` and filtered by `company_id`
            and `form_id`
        """
        return self.get_queryset().filter(
            company_id=company_id, 
            form_id=form_id
        ).order_by('-updated_at')

    def dynamic_forms_by_company_id_form_id_between_updated_at_range_ordered_by_updated_at(
        self, company_id, form_id, updated_at_start_date, updated_at_end_date
    ):
        """
        Similar to `dynamic_forms_by_company_id_and_form_id_orderd_by_updated_at` method but also
        filtered by a range of update_at dates.

        Args:
            company_id (int): This is a Company instance id.
            form_id (int): A reflow_server.formulary.models.Form instance id to filter
                           the DynamicForm
            updated_at_start_date (datetime.datetime): A datetime instance of the start date of 
                                                       the updated_at search. Since we filter by a range
                                                       of dates we need both the start_date and end_date
                                                       of the `updated_at`
            updated_at_end_date (datetime.datetime): A datetime instance of the end date of 
                                                     the udated_at search. 
        Returns:
            django.db.models.QuerySet(reflow_server.data.models.DynamicForm): A queryset
            of ordered DynamicForm instances by `updated_at` and filtered by `company_id`
            and `form_id`
        """
        return self.dynamic_forms_by_company_id_and_form_id_orderd_by_updated_at(company_id, form_id)\
            .filter(
                updated_at__range=[updated_at_start_date, updated_at_end_date],
            )

    def dynamic_forms_by_dynamic_form_ids_ordered(self, dynamic_form_ids):
        """
        Gets an Queryset of DynamicForm instances ordered by dynamic_form_ids.
        These dynamic_form_ids are a list of DynamicForm instance ids. These ids
        will be ordered

        Args:
            dynamic_form_ids (list(int)): List of ORDERED DynamicForm instance ids. 

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.DynamicForm): A queryset
            of ordered DynamicForm instances filtered and order by `dynamic_form_ids` parameter
            recieved.
        """
        order = Case(*[When(id=form_data_id, then=index) for index, form_data_id in enumerate(dynamic_form_ids)])
        return self.get_queryset().filter(id__in=dynamic_form_ids).order_by(order)

    def dynamic_form_ids_by_depends_on_id_and_company_id(self, depends_on_id, company_id):
        """
        Gets dynamic_form_ids by depends_on_id, so in other words it gets the sections
        of a main formulary.

        Args:
            depends_on_id (int): The main formulary id, its a DynamicForm instance id with
                                 depends_on as NULL.
            company_id (int): The company id this form data is from.

        Returns:
            django.db.models.QuerySet(int): A queryset where each element is an id of a section.
                                            in other words, each ID is a DynamicForm instance id
        """
        return self.get_queryset().filter(
            company_id=company_id, 
            depends_on=depends_on_id
        ).values_list('id', flat=True)

    def remove_dynamic_form_by_dynamic_form_id_company_id_and_form_name(
        self, dynamic_form_id, company_id, form_name
    ):
        """
        Removes a DynamicForm instance based on the dynamic_form_id, the company_id and
        a form_name. HEY BUT WHY DON'T WE NEED THE FORM_NAME? It actually works a last resort
        it prevents us from deleting form_data of a different form. This way the user needs to know
        more data than just a dynamic_form_id and a company_id to delete a formulary data.

        Args:
            dynamic_form_id (int): The id of the DynamicForm instance you want to delete
            company_id (int): The company id from who this DynamicForm is from.
            form_name (str): The form name of whose form this data is from.
        """
        return self.dynamic_form_by_dynamic_form_id_and_company_id(dynamic_form_id, company_id, form_name)\
            .delete()

    def remove_dynamic_forms_from_enabled_forms_and_by_depends_on_id_and_conditional_excludes_data_if_not_setexcluding_dynamic_form_ids(
        self, depends_on_id, dynamic_form_ids
    ):
        return self.get_queryset().filter(
            form__enabled=True, 
            form__conditional_excludes_data_if_not_set=True,
            depends_on_id=depends_on_id
        )\
            .exclude(id__in=dynamic_form_ids)\
            .delete()