from django.conf import settings

from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection

from asgiref.sync import async_to_sync

import json


def get_consumers(key):
    """
    Function used for retrieving consumers to your base consumer.
    """
    method_list = list()
    kls_list = list()
    for consumer in settings.CONSUMERS[key]:
        striped = consumer.split('.')
        kls_name = striped.pop(-1)
        path = '.'.join(striped)
        module = __import__(path, fromlist=[kls_name])
        kls = getattr(module, kls_name)
        kls_list.append(kls)
        kls_methods_list = [func for func in dir(kls) if callable(getattr(kls, func)) and not func.startswith("__")]
        if any([method in method_list for method in kls_methods_list]):
            raise AttributeError('Your consumer methods MUST BE unique, found a duplicate method in the following consumer: {}'.format(consumer))
        else:
            method_list = method_list + kls_methods_list
    return tuple(kls_list)


class BaseConsumer(WebsocketConsumer):
    """
    This is the base consumer, ALL OF YOUR CONSUMER MUST INHERIT from this class. This adds a simple
    change to the default django channel consumers.

    With this your consumers become simple python classes that MUST be registered in CONSUMERS dict in your
    `settings.py`. Look at the example below for more detais.

    This class is not meant to be used in `routing.py`.

    With this all the data you recieve "FROM" and send "TO" a client must contain a "type" key in the json to identify the event.
    This `type` is used for sending to the handler method. Your handler methods must contain the `recieve_` 
    keyword in the start of the method.
    
    So for example, if you have a consumer like this in your `notifications.consumers.py`:
    >>> class NotificationConsumer:
            def send_notification(self, event):
                #...your code here
            def recieve_notification(self, data):
                #...your code here
            def recieve_notification_configuration(self, data):
                #... your code here
    
    You need first to register it in `settings.py` `CONSUMERS`:
    >>> CONSUMERS = {
        'LOGIN_REQUIRED': [
            'reflow_server.notifications.consumers.NotificationConsumer'
        ]
    }

    To recieve data from the client in the method `.recieve_notification()` your data must be like the following:
    >>> { 
            'type': 'notification',
            'data': 'foo'
        }
    
    To recieve data from the client in the method  `.recieve_notification_configuration()` your data must be like the following:
    >>> { 
            'type': 'notification_configuration',
            'data': 'bar'
        }
    
    The method `.send_notification()` is not a handler, it is used to send data to your clients, you can refer to documentation here: 
    https://stackoverflow.com/a/50048713/13158385
    https://channels.readthedocs.io/en/latest/topics/channel_layers.html#what-to-send-over-the-channel-layer
    https://channels.readthedocs.io/en/latest/topics/channel_layers.html#groups
    https://channels.readthedocs.io/en/latest/topics/channel_layers.html#using-outside-of-consumers


    __IMPORTANT__:
    - To recieve data, your methods MUST contain the `recieve_` keyword. 
    - Your methods must always be unique.
    - Don't forget to register your consumers in `settings.py` with the CONSUMERS list tag.
    """
    group_name = 'default'


    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        print('Closing Group name: %s' % self.group_name)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        action_type = data['type']
        handler = getattr(self, 'recieve_%s' % action_type, None)
        if handler:
            handler(data['data'] if 'data' in data else dict())
        else:
            self.send(text_data=json.dumps({
                'status': 'error',
                'reason': 'no_handler_found_for_type' 
            }))

    @classmethod
    def send_event(cls, event_name, group_name, **kwargs):
        if not hasattr(event_name, cls):
            raise KeyError('Seems like there is no handler for %s event' % event_name)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            '{}'.format(group_name),
            {
                'type': event_name,
                'data': kwargs
            }
        )


class UserConsumer(BaseConsumer, *get_consumers('LOGIN_REQUIRED')):
    """
    This class is a Consumer that we use in our root routing.py, this consumer is used for 
    validating before connecting. 
    
    To use this consumer you must declare your consumer inside of the 'LOGIN_REQUIRED' 
    key of the CONSUMERS dict in `settings.py`
    
    You can create your own custom consumers inherinting the class from 
    (BaseConsumer, *get_consumers(YOUR_CUSTOM_KEY_IN_CONSUMERS)). In `settings.py`, in the CONSUMERS 
    dict, you must add a key that will default to your custom consumer.

    So, if you want to add a consumer that validates if the `company_id` is defined prior connecting 
    you create something like this:

    in `settings.py`: 
    >>> CONSUMERS = {
        # other keys
        'COMPANY_REQUIRED': [
            # your consumers
        ]
    }

    in `core.consumers.py`:
    >>> class CompanyConsumer(BaseConsumer, *get_consumers('COMPANY_REQUIRED')):
            def connect(self):
                # your custom connect logic here

    and in root `routing.py`:
    >>> application = ProtocolTypeRouter({
        'websocket': AuthWebsocketJWTMiddleware(
            URLRouter([
                # other consumers
                re_path(r'^websocket/custom_route_to_your_consumer', CompanyConsumer)
            ])
        )
    })
    """
    group_name = 'user_{id}'

    def connect(self):
        if 'user' in self.scope and self.scope['user'].is_authenticated:
            # we create a custom group_name for each user, so when we send 
            # events we can send them to a specific user.
            self.group_name = self.group_name.format(id=self.scope['user'].id)
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )
            self.accept()
        else:
            raise DenyConnection('For `user` group types, your user must be authenticated')
    
    @classmethod
    def send_event(cls, event_name, user_id, **kwargs):
        group_name = cls.group_name.format(id=user_id)
        super().send_event(event_name, group_name, **kwargs)