from django.conf.urls import re_path, include

from reflow_server.core.decorators import permission_required, authorize_external_response
from reflow_server.data.views import FormularyDataView


urlpatterns = [
    re_path(r'(?P<company_id>\w+\.\w+)/(?P<form>\w+)/$', permission_required(FormularyDataView.as_view()), name='formulary_formulary_data_view')
]