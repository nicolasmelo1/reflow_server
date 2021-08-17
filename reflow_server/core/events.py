from django.conf import settings


class Event:
    """
    This works really simple, first we set the event we want to keep track of in the EVENTS setting in settings.py.

    To consume events you must declare consumers in a 'events.py' file. This file is responsible for consuming events, and while consuming events you can do almost
    everything you want, you can track, you can log or you can even dispatch automations. Beware, events.py should NOT CONTAIN ANY BUSINESS LOGIC, Business logic should still 
    be handled in services.

    You will set the event as a dict like:

    'formulary_data_created': {
        'data_parameters': ['user_id', 'company_id', 'form_id', 'form_data_id'],
        'consumers': ['reflow_server.data.events.DataEvents']
    }

    The first key is the name of the event, it is important to notice that is always separated by an underline. This is because the consumers of this will 
    NEED TO HAVE A STATICMETHOD with the exact value of the string.

    Inside the event name key we have two DEFAULT keys:
    
    - `data_parameters`: This is all of the keys the dict this event recieves must contain.
                         so in the example above, when registering the 'formulary_data_created' event the `data` dict must be
                         structured like the following:

    >>> {
        'user_id': 1231,
        'company_id': 123123,
        'form_id': 123123123,
        'form_data_id': 5235235
    }

    if just one key is missing from the data, the event will throw an error. 
    IMPORTANT: Notice that this doesn't validate dict inside a dict, so try to keep your event data as flat as possible: Just one event.

    - `consumers`: we will have an array of consumers, this way whenever we send a new event, we can distribute this event to multiple consumers at once.
                   The consumers must be the complete location to the file.

    "THIS LOOKS LIKE A WET ARCHITECTURE, WHY DON'T YOU GUYS USE SIGNALS? SO MUCH EASIER"
    First: on signals everything works implicitily, you send signals trough the code, you recieve signals in signals. 
    But you are not able to know what was calling this signal. I mean, i don't know if this came from a formulary that was updated, or if this was called from a user that
    just made login. I can't track. And since i can't track this is not a good solution. Evend Django acknowledge that signals might be hard to debug.
    https://docs.djangoproject.com/en/dev/topics/signals/#defining-and-sending-signals (see the blue square)

    On this solution on the other hand you can know what data you will recieve, where the code that consumes this event is located, and so on. Everything
    is declared explicitly to the programmer, so it is a LOT EASIER to maintain and extend.

    The Consumer will look something like:

    >>> class DataEvent:
            def formulary_data_created(self, user_id, company_id, form_id, form_data_id):
                # code here

    Super simple, actually.

    After that all, to fire events use `.register_event()` for dispatching to the consumers like:
    >>> from reflow_server.core.event import Event
    >>> Event.register_event('formulary_data_created', {
        'user_id': 1231,
        'company_id': 123123,
        'form_id': 123123123,
        'form_data_id': 5235235
    })

    IMPORTANT: Remember that `data_parameters` holds all of the data that obligatory needs to be passed. So be aware that you are sending all of the data needed.
    """
    @staticmethod
    def register_event(event_name, data):
        if event_name in settings.EVENTS:
            Event.validate_data(event_name, data)

            event_settings = settings.EVENTS[event_name]

            for consumer in event_settings['consumers']:
                striped = consumer.split('.')
                kls_name = striped.pop(-1)
                path = '.'.join(striped)
                module = __import__(path, fromlist=[kls_name])
                kls = getattr(module, kls_name)
                kls_instance = kls()
                if hasattr(kls_instance, event_name):
                    handler = getattr(kls_instance, event_name)
                    handler(**data)
                else:
                    raise KeyError("'{kls_name}' has no method named '{event_name}'".format(kls_name=kls, event_name=event_name))
                
        else:
            raise ValueError("'{event_name}' was not defined in 'EVENT' setting in 'settings.py'".format(event_name=event_name))
    
    @staticmethod
    def validate_data(event_name, data):
        """
        Validates if the data that is being passed to the consumers acknowledge the 'data_parameters' definition for the event
        otherwise throws an error. Saying that the data is incomplete. This guarantees the data passed is exactly shaped as it was defined.
        So the function that recieves the data doesn't have any surprises.

        Args:
            event_name (str): The name of the event that is being fired.
            data (dict): The dict holding the data, be aware that this dict must have the keys defined in `data_parameters` if it is any different it
                         will throw an error.

        Raises:
            KeyError: Throws an error if the data passed is not the same as the `data_parameters` defined in the EVENTS setting in `settings.py`
        """
        event_settings = settings.EVENTS.get(event_name, None)
        if event_settings:
            for parameter in event_settings['data_parameters']:
                if parameter not in data:
                    raise KeyError(
                        "'{event_name}' data contains the following parameters: [{parameters}]. Looks like you forgot '{parameter}' parameter".format(
                            event_name=event_name,
                            parameters=', '.join(event_settings['data_parameters']),
                            parameter=parameter
                        )
                    )
