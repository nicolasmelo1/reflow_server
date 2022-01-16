from django.urls import re_path
from reflow_server.integration.views import IntegrationAuthenticationView


urlpatterns = [
    re_path(r'^(?P<service_name>\w+)/$', IntegrationAuthenticationView.as_view(), name='integration_authentication_view'),
]
