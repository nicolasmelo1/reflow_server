from django.db import models
from django.db.models import Q


class FormValueKanbanManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()
    
    def form_value_by_form_value_id(self, form_value_id):
        """
        Gets a single instance based on a FormValue instance id

        Args:
            form_value_id (int): the id of the form value instance

        Returns:
            reflow_server.data.models.FormValue: The FormValue instance
        """
        return self.get_queryset().filter(id=form_value_id).first()
    
    def form_values_by_dynamic_form_id(self, dynamic_form_id):
        """
        Gets a queryset of FormValue instances based on a dynamic_form_id. This dynamic_form_id is the id
        of the section data it was saved.

        Args:
            dynamic_form_id (int): This is an id of a DynamicForm instance where the depends_on column is NOT equal
                                   to null

        Returns:
            django.db.models.QuerySet(reflow_server.data.models.FormValue): A queryset of FormValue instances 
                                                                            based on the parameters
        """
        return self.get_queryset().filter(form_id=dynamic_form_id)

    def distinct_values_by_depends_on_ids_and_field_id_excluding_null_and_empty(self, depends_on_ids, field_id):
        """
        Gets a QuerySet of values instances from the field_id, the field_type_id and 
        The queryset here doesn't comply NULL or EMPTY values.

        Args:
            depends_on_ids (list(int)): This is a list of main formulary ids and not section ids from what forms you want to retrieve this FormValues from
            field_id (int): The id of the field of the FormValue

        Returns:
            django.db.models.QuerySet(str): This is a queryset of values of the FormValue instances
        """
        return self.get_queryset().filter(
            form__depends_on_id__in=depends_on_ids, 
            field_id=field_id, 
        ).exclude(
            Q(value='') | Q(value__isnull=True)
        ).values_list('value', flat=True).distinct()

    def distinct_values_by_dynamic_forms_and_field(self, dynamic_forms, field):
        """
        Gets distinct values of FormValue instaces by a list of dynamic_forms and a Field instance. 
        These dynamic_forms are the DynamicForm instances with depends_on NOT NULL. So it's the sections 
        of the data.

        Args:
            dynamic_form_ids (list(reflow_server.data.model.DynamicForm)): The instances of DynamicForm model
            field (reflow_server.formulary.model.Field): The instance of Field model

        Returns:
            django.db.model.QuerySet(str): Returns a queryset of strings, each string is a value from a FormValue instance
        """
        return self.get_queryset().filter(
            form__in=dynamic_forms, 
            field=field
        ).values_list('value', flat=True).distinct()

    