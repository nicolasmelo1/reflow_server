from django.db import transaction

from reflow_server.core.utils.asynchronous import RunAsyncFunction
from reflow_server.analytics.models import TypeOfEvent, Event, EventData
from reflow_server.analytics.services.mixpanel import MixpanelService


class AnalyticsService:
    def __init__(self):
        self.mixpanel_service = MixpanelService()

    def dispatch_to_mixpanel(self, event_name, event_data):
        async_task = RunAsyncFunction(self.mixpanel_service.dispatch_event)
        async_task.delay(event_name=event_name, event_data=event_data)

    @transaction.atomic
    def register_event(self, event_name, **kwargs):
        """
        Registering an event means saving the event in our database so we can log it whenever we want and
        whenever it is needed.

        For every event you dispatch using the 'reflow_server.core.events.Event' class we will
        add the `reflow_server.analytics.events.AnalyticsEvent` listener so we ca save those events
        on `event` table, this way internally we can make queries to know what the user is doing 
        in our platform in almost real time.

        After saving the event internally we dispatch it to other platforms.
        
        Args:
            event_name (str): The name of the event, usually the event_name are the keys defined in the
                              EVENTS setting in `settings.py`
        """
        type_of_event_instance = TypeOfEvent.analytics_.type_of_event_by_event_name(event_name)
        does_exist_type_of_event = type_of_event_instance == None

        if does_exist_type_of_event:
            type_of_event_instance = TypeOfEvent.analytics_.create_type_of_event(event_name)
        
        event_instance = Event.analytics_.create_event(type_of_event_id=type_of_event_instance.id)

        event_datas = []
        for key, value in kwargs.items():
            event_datas.append(
                EventData(
                    event=event_instance,
                    parameter_name=key, 
                    value=str(value)
                )
            )

        EventData.objects.bulk_create(event_datas)
        self.dispatch_to_mixpanel(event_name, kwargs)
