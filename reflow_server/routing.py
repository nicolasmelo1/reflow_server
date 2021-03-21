from django.urls import re_path

from channels.routing import URLRouter

from reflow_server.core.consumers import UserConsumer, PublicConsumer
from reflow_server.authentication.middleware import AuthWebsocketJWTMiddleware, AuthWebsocketPublicMiddleware

websocket_urlpatterns = [
    re_path(r'^websocket/', URLRouter([
        re_path(r'user/$', AuthWebsocketJWTMiddleware(UserConsumer.as_asgi())),
        re_path(r'public/$', AuthWebsocketPublicMiddleware(PublicConsumer.as_asgi()))
    ]))
]
