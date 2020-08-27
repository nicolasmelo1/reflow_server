from django.db import models
from django.db.models import Case, When

class FormValueListingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

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
    