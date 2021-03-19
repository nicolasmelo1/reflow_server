from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.data.views import FormularyDataView, FormularyDataEditView, DataView, DownloadFileView


urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^all/$', validate_billing(DataView.as_view())),
        re_path(r'^$', validate_billing(FormularyDataView.as_view()), name='formulary_formulary_data_view'),
        re_path(r'^(?P<dynamic_form_id>\d+)/$', validate_billing(FormularyDataEditView.as_view()), name='formulary_formulary_data_edit_view'),
        re_path(r'^(?P<dynamic_form_id>\d+)/(?P<field_id>\d+)/(?P<file_name>.+)/$', validate_billing(DownloadFileView.as_view()), 
            name='formulary_download_file_view'
        )
    ]))
]