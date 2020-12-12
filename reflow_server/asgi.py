"""
ASGI config for reflow_server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""


from django import setup
from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter

import os


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reflow_server.settings")

setup()

from reflow_server.authentication.middleware import AuthWebsocketJWTMiddleware

from .routing import websocket_urlpatterns

# Read here for reference: https://channels.readthedocs.io/en/stable/tutorial/part_2.html#write-your-first-consumer
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthWebsocketJWTMiddleware(
        URLRouter(websocket_urlpatterns)
    )
})
