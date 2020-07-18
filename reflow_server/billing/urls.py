from django.conf.urls import re_path, include
from django.conf import settings

from reflow_server.core.utils.routes import register_attachment_url

from reflow_server.core.decorators import validate_billing
from reflow_server.billing.views import VindiWebhookView, GetTotalView



vindi_urlpatterns = [
    re_path(r'^webhook/$', VindiWebhookView.as_view(), name='billing_vindi_webhook_view')
]

urlpatterns = [
    register_attachment_url(re_path(r'^total/(?P<company_id>\d+)/$', validate_billing(GetTotalView.as_view()), name='billing_get_total_view')),
    re_path(r'^vindi/', include(vindi_urlpatterns), name='billing_vindi')
]
