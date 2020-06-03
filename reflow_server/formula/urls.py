from django.conf.urls import re_path

from reflow_server.core.decorators import permission_required
from reflow_server.core.utils.routes import register_admin_only_url
from reflow_server.formula.views import TestFormulaView

adminonly_urlpatterns = [
    register_admin_only_url(
        re_path(r'^(?P<company_id>\w+\.\w+)/(?P<form_id>\d+)/$', permission_required(TestFormulaView.as_view()), name='formula_test_formulas')
    )
]

urlpatterns = adminonly_urlpatterns