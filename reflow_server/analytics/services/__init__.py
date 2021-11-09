from django.db import transaction

from reflow_server.core.utils.asynchronous import RunAsyncFunction
from reflow_server.analytics.models import TypeOfEvent, Event, EventData
from reflow_server.analytics.services.mixpanel import MixpanelService

import collections


class AnalyticsService:
    def __init__(self):
        self.mixpanel_service = MixpanelService()
    # ------------------------------------------------------------------------------------------
    def format_request_event(self, event_data, parent_key='', separator='_'):
        """
        Formats the data of the event of a request. Since we don't trust that the front-end will give us the formatted data
        we need to format it so it doesn't become nested. (yeah, i don't trust anyone, not even myself https://i.kym-cdn.com/entries/icons/facebook/000/017/046/BptVE1JIEAAA3dT.jpg)

        Reference: https://stackoverflow.com/a/6027615

        Args:
            event_name (str): The name of the event. This is one of the keys in 'EVENTS' setting in `settings.py`.
            event_data (dict): The data of the event, the keys are defined in 'EVENTS' setting with the 'data_parameters' key.
        
        Returns:
            dict: Returns a formated dict
        """
        items = []
        for key, value in event_data.items():
            new_key = parent_key + separator + key if parent_key != '' else key
            if isinstance(value, collections.MutableMapping):
                items.extend(self.format_request_event(value, new_key, separator=separator).items())
            else:
                items.append((new_key, value))
        return dict(items)
    # ------------------------------------------------------------------------------------------
    def dispatch_to_mixpanel(self, event_name, event_data):
        """
        Dispatch the event to mixpanel so mixpanel can track the user inside our platform. Although we send events
        to mixpanel, most of the events can be tracked inside of the reflow application.

        Args:
            event_name (str): The name of the event. This is one of the keys in 'EVENTS' setting in `settings.py`.
            event_data (dict): The data of the event, the keys are defined in 'EVENTS' setting with the 'data_parameters' key.
        """
        async_task = RunAsyncFunction(self.mixpanel_service.dispatch_event)
        async_task.delay(event_name=event_name, event_data=event_data)
    # ------------------------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------------------------
