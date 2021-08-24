from django.conf.urls import re_path, include

from reflow_server.filter.views import TestarFilter


urlpatterns = [
    re_path(r'^$', TestarFilter.as_view(), name='filter_test')
]