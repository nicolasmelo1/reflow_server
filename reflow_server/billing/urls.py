from django.conf.urls import re_path, include
from django.conf import settings

from reflow_server.core.utils.routes import register_admin_only_url

from reflow_server.core.decorators import permission_required
from reflow_server.billing.views import CurrentCompanyChargeView, PaymentView, VindiWebhookExternalView, GetTotalView



vindi_urlpatterns = [
    re_path(r'^webhook/$', VindiWebhookExternalView.as_view(), name='billing_vindi_webhook_view')
]

external_urlpatterns = [
    re_path(r'^vindi/', include(vindi_urlpatterns))
]

settings_urlpatterns = [
    re_path(r'^$', permission_required(CurrentCompanyChargeView.as_view()), name='billing_charge_view'),
    re_path(r'^payment/$', permission_required(PaymentView.as_view()), name='billing_payment_view')
]

urlpatterns = [
    re_path(r'^(?P<company_id>(\w+(\.)?(-)?(_)?)+)/', include([
        register_admin_only_url(re_path(r'^settings/', include(settings_urlpatterns))),
    ])),
    re_path(r'^external/', include(external_urlpatterns))
]
