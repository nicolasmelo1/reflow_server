from django.urls import re_path

from reflow_server.core.consumers import UserConsumer

websocket_urlpatterns = [
    re_path(r'^websocket/', UserConsumer.as_asgi()),
]
