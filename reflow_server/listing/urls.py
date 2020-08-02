from django.conf.urls import re_path, include
from django.conf import settings

from reflow_server.core.decorators import validate_billing, authorize_external_response
from reflow_server.listing.views import ListingHeaderView, GetExtractDataView, ExtractDataBuilderView, ExtractFileExternalView

external_urlpatterns = [
    re_path(r'^extract/(?P<company_id>\d+)/(?P<user_id>\d+)/(?P<form_name>\w+)/$', authorize_external_response(ExtractFileExternalView.as_view()), name='listing_external_file_data'),
]

urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/', include([
        re_path(r'^extract/(?P<file_id>[\w-]+)/$', validate_billing(GetExtractDataView.as_view()), name='listing_get_extract_data'),
        re_path(r'^(?P<form>\w+)/', include([
             re_path(r'^$', validate_billing(ListingHeaderView.as_view()), name='listing_get_header'),
             re_path(r'^extract/$', validate_billing(ExtractDataBuilderView.as_view()), name='listing_build_extract_data'),    
        ])),
    ])),
    re_path(r'^external/', include(external_urlpatterns))
]