from django.conf.urls import re_path, include

from reflow_server.authentication.services.routes import register_can_be_public_url
from reflow_server.core.decorators import validate_billing, authorize_external_response
from reflow_server.data.views import FormularyDataView, FormularyDataEditView, DataView, DownloadFileView, \
    APIConfigurationLastValueForFieldDataView
from reflow_server.data.views.external import ExtractFileExternalView
from reflow_server.data.views.extract import GetExtractDataView, ExtractDataBuilderView


external_urlpatterns = [
    re_path(r'^extract/(?P<company_id>\d+)/(?P<user_id>\d+)/(?P<form_name>\w+)/$', 
        authorize_external_response(ExtractFileExternalView.as_view()), name='data_external_file_data'),
]

urlpatterns = [
    re_path(r'^external/', include(external_urlpatterns)),
    re_path(r'(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^extract/', include([
            re_path(r'^$', validate_billing(ExtractDataBuilderView.as_view()), name='data_build_extract_data'), 
            re_path(r'^(?P<file_id>[\w-]+)/$', validate_billing(GetExtractDataView.as_view()), name='data_get_extract_data')
        ])),
        re_path(r'^all/$', validate_billing(DataView.as_view()), name='data_retrieve_data_view'),
        re_path(r'^api_configuration/last_values/$', validate_billing(APIConfigurationLastValueForFieldDataView.as_view()), name='data_api_configuration_last_values_for_fields_view'),
        register_can_be_public_url(re_path(r'^$', validate_billing(FormularyDataView.as_view()), name='formulary_formulary_data_view')),
        re_path(r'^(?P<dynamic_form_id>\d+)/$', validate_billing(FormularyDataEditView.as_view()), name='formulary_formulary_data_edit_view'),
        re_path(r'^(?P<dynamic_form_id>\d+)/(?P<field_id>\d+)/(?P<file_name>.+)/$', validate_billing(DownloadFileView.as_view()), 
            name='formulary_download_file_view'
        )
    ]))
]