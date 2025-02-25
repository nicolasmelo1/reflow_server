from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing, authorize_external_response
from reflow_server.draft.views import DraftSaveFileView, DraftSaveValueView, DraftEditFileView, DraftRemoveDraftView
from reflow_server.draft.views.externals import DraftRemoveDraftExternalView, APIDraftSaveFileExternalView
from reflow_server.draft.services.routes import register_draft_url
from reflow_server.authentication.services.routes import register_can_be_public_url
from reflow_server.authentication.decorators import api_token_required


external_urlpatterns = [
    re_path(r'api/(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/$', api_token_required(APIDraftSaveFileExternalView.as_view()), name='api_external'),
    re_path(r'remove_old_drafts/$', authorize_external_response(DraftRemoveDraftExternalView.as_view()), name='draft_external_remove_old_drafts_view')
]

urlpatterns = [
    re_path(r'external/', include(external_urlpatterns)),
    re_path(r'(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/', include([
        register_can_be_public_url(register_draft_url(re_path(r'^file/', include([
            re_path(r'^$', validate_billing(DraftSaveFileView.as_view()), name='draft_save_file_draft_view'),
            re_path(r'^(?P<draft_string_id>^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)/$', validate_billing(DraftEditFileView.as_view()), name='draft_edit_file_draft_view'),
        ])))),
        re_path(r'^value/$', validate_billing(DraftSaveValueView.as_view()), name='draft_save_value_draft_view'),
        register_can_be_public_url(
            re_path(r'^(?P<draft_string_id>^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)/', include([
                re_path(r'^$', validate_billing(DraftRemoveDraftView.as_view()), name='draft_remove_draft_view'),
            ]))
        )
    ]))
]