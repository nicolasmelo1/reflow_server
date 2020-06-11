from django.conf.urls import re_path, include

from reflow_server.core.decorators import permission_required, authorize_external_response
from reflow_server.data.views import FormularyDataView, FormularyDataEditView, DataView


urlpatterns = [
    re_path(r'(?P<company_id>\w+\.\w+)/(?P<form>\w+)/', include([
        re_path(r'^all/$', permission_required(DataView.as_view())),
        re_path(r'^$', permission_required(FormularyDataView.as_view()), name='formulary_formulary_data_view'),
        re_path(r'^(?P<dynamic_form_id>\d+)$', permission_required(FormularyDataEditView.as_view()), name='formulary_formulary_data_edit_view')
    ]))
]