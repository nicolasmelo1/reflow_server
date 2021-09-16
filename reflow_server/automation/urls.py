from django.conf.urls import re_path, include

from reflow_server.automation.views import AutomationWebhookVersion1View

urlpatterns = [
    re_path(r'^webhook/v1/(?P<app_name>\w+)/(?P<automation_trigger_name>\w+)/(?P<user_id>\d+)/$', AutomationWebhookVersion1View.as_view(), name='automation_v1_webhook')
]