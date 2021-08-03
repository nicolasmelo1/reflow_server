from django.db import models


class EventAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_event(self, type_of_event_id):
        """
        Creates a new event in our database so that we know an event was dispatched. With this
        we can track what happened in our platform. 

        This makes it easier for logging purposes and also for tracking what the user had done inside
        of reflow.

        Args:
            type_of_event_id (int): The TypeOfEvent instance id so we know what event was issued.

        Returns:
            reflow_server.analytics.models.Event: Returns the created Event instance.
        """
        return self.get_queryset().create(type_of_event_id=type_of_event_id)