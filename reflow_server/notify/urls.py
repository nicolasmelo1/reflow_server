from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.notify.views import RegisterPushNotificationEndpointView

urlpatterns = [
    re_path(r'^push_notification/$', validate_billing(RegisterPushNotificationEndpointView.as_view()), name='notify_register_push_notification')
]