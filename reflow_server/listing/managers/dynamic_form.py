from django.db import models
from django.db.models import Case, When

class DynamicFormListingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
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
