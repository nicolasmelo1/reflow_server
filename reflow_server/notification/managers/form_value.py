from django.conf import settings
from django.db import models
from django.db.models import DateTimeField, Value, ExpressionWrapper, Case, When, Func, F
from django.db.models.functions import Now

from datetime import timedelta


class FormValueNotificationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().all()

    def form_value_by_main_formulary_data_id_and_field_id(self, formulary_data_id, field_id):
        """
        This gets the first FormValue instance by a single field_id and a main formulary_data_id. This main_formulary_data_id
        is the id of the DynamicForm that has depends_on column as NULL. So not the sections saved but the main 
        formulary data.

        Args:
            formulary_data_id (int): the main_formulary_data_id. These are the DynamicForm instances that have
                                     depends_on_id equal to None
            field_id (int): The field_id to get the data from

        Returns:
            reflow_server.data.models.FormValue: The FormValue instance
        """
        return self.get_queryset().filter(
            field_id=field_id, 
            form__depends_on_id=formulary_data_id
        ).first()


    def create_reminders_based_on_data_saved(self, main_form_data_ids, field, days_diff=0, timezone=0):
        # it is important to notice that on the annotate we convert the value to the same date as the server
        # so when we filter, we already got the server time so no need to add or subtract timedelta.
        # The annotate is not straight forward actually, but we NEED a CASE WHEN clause to convert the dates
        # since when we filter the values converting we might face some errors because the filter actually get all the values
        # while filtering it means WHERE field_type = 'date' AND to_timestamp('value') = CURRENT_TIMESTAMP does not work, 
        # because the data is not yet filtered with only field_type='date' while doing the second filter, that's why 
        # we need a case when, this way all of the values that are not of type 'date' become NULL, so we can perform the second 
        # filter without errors.
        return self.get_queryset().filter(
                form__depends_on_id__in=main_form_data_ids, field=field, field_type__type='date'
            ).annotate(
                value_as_date=Case(
                    When(
                        field_type__type='date', 
                        then=ExpressionWrapper(
                            Func(
                                F('value'),
                                Value(settings.DEFAULT_PSQL_DATE_FIELD_FORMAT), 
                                function='to_timestamp'
                            ) + timedelta(days=days_diff) - timedelta(hours=timezone),
                            output_field=DateTimeField()
                        )
                    ),
                    default=None
                )                                           
            ).filter(
                value_as_date__gte=Now()
            ).values_list('value_as_date','form__depends_on_id')