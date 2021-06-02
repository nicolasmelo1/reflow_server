from django.conf.urls import re_path

from reflow_server.core.decorators import validate_billing
from reflow_server.authentication.services.routes import register_admin_only_url
from reflow_server.formula.views import TestFormulaView

adminonly_urlpatterns = [
    register_admin_only_url(
        re_path(r'^(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/(?P<form_id>\d+)/$', validate_billing(TestFormulaView.as_view()), name='formula_test_formulas')
    ),
]

urlpatterns = adminonly_urlpatterns