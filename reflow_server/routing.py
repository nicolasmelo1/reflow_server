from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from reflow_server.middleware import AuthWebsocketJWTMiddleware
from reflow_server.core.consumers import UserConsumer

application = ProtocolTypeRouter({
    'websocket': AuthWebsocketJWTMiddleware(
        URLRouter([
            re_path(r'^websocket/', UserConsumer)
        ])
    )
})

