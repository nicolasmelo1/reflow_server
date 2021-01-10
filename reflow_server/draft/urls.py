from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.draft.views import DraftSaveFileView, DraftSaveValueView, DraftEditFileView, DraftRemoveDraftView

urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/', include([
        re_path(r'^file/', include([
            re_path(r'^$', validate_billing(DraftSaveFileView.as_view()), name='draft_save_file_draft_view'),
            re_path(r'^(?P<draft_string_id>^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)/$', validate_billing(DraftEditFileView.as_view()), name='draft_edit_file_draft_view')
        ])),
        re_path(r'^value/$', validate_billing(DraftSaveValueView.as_view()), name='draft_save_value_draft_view'),
        re_path(r'^(?P<draft_string_id>^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)/$', validate_billing(DraftRemoveDraftView.as_view()), name='draft_remove_draft_view')
    ]))
]