from django.conf.urls import re_path

from reflow_server.core.decorators import validate_billing
from reflow_server.listing.views import ListingHeaderView


urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/(?P<form>\w+)/$', validate_billing(ListingHeaderView.as_view()), name='listing_get_header')
]