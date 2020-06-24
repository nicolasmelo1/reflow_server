from django.conf.urls import re_path, include

from reflow_server.analytics.views import TestAggregation

urlpatterns = [
    re_path(r'^(?P<method_type>\w+)/$', TestAggregation.as_view())
]


