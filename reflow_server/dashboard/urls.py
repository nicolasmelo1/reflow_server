from django.conf.urls import re_path, include

from reflow_server.core.decorators import permission_required
from reflow_server.dashboard.views import DashboardChartConfigurationView

settings_urlpatterns = [
    re_path(r'^$', permission_required(DashboardChartConfigurationView.as_view()), name='dashboard_chart_configuration')
]

urlpatterns = [
    re_path(r'^(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^settings/', include(settings_urlpatterns))
    ]))
]


