from django.db import models


class TypeOfEventAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_type_of_event(self, event_name):
        """
        Everytime an event is dispatched we create it in the TypeOfEvent model since
        we don't have control on what events are dispatched inside of the reflow platform.

        The programmer just defines it in the 'EVENTS' setting in the 'settings.py' file, because 
        of that, this needs to work automatically, everytime an event is dispatched with an new name
        we save it to the TypeOfEvent model.

        Args:
            event_name (str): The new event_name to save.
        
        Returns:
            reflow_server.analytics.model.TypeOfEvent: The newly created TypeOfEvent instance
        """
        return self.get_queryset().create(event_name=event_name)

    def type_of_event_by_event_name(self, event_name):
        """
        Tries to fetch a TypeOfEvent model by it's name, if it returns None it doesn't exist, so you
        need to use `.create_type_of_event()` function. Otherwise just save this in the Event table.

        Args:
            event_name (str): The name of the event to save.

        Returns:
            [None, reflow_server.analytics.model.TypeOfEvent]: Returns None if the TypeOfEvent doesn't exists or
                                                               or the TypeOfEvent instance if it does.
        """
        return self.get_queryset().filter(event_name=event_name).first()