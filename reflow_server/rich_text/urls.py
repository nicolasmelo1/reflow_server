from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.rich_text.views import RichTextDataView

# TODO: SECURITY ISSUE, MAKE THIS MORE SECURE
urlpatterns = [
    re_path(r'^(?P<page_id>\d+)/$', RichTextDataView.as_view(), name='rich_text_test_view')
] 