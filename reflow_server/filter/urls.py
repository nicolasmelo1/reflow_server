from django.conf.urls import re_path, include

from reflow_server.filter.views import TestSearchFilterView, TesValidateFilterView


urlpatterns = [
    re_path(r'^test_search/$', TestSearchFilterView.as_view(), name='filter_search_test'),
    re_path(r'^test_validate/$', TesValidateFilterView.as_view(), name='filter_validate_test')
]