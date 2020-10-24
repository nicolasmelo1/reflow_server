from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.rich_text.views import TestTextView

urlpatterns = [
    re_path(r'^test_text/(?P<page_id>\d+)/$', TestTextView.as_view(), name='rich_text_test_view')
] 