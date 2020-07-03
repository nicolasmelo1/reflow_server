from django.conf.urls import re_path, include

from reflow_server.core.decorators import permission_required
from reflow_server.dashboard.views import DashboardChartConfigurationView, DashboardChartConfigurationEditView, \
    DashboardFieldsView, DashboardChartsView, DashboardDataView

settings_urlpatterns = [
    re_path(r'^$', permission_required(DashboardChartConfigurationView.as_view()), name='dashboard_chart_configuration'),
    re_path(r'^(?P<dashboard_configuration_id>\d+)/$', permission_required(DashboardChartConfigurationEditView.as_view()), name='dashboard_chart_edit_configuration'),
    re_path(r'^field_options/$', permission_required(DashboardFieldsView.as_view()), name='dashboard_fields_configuration')
]

urlpatterns = [
    re_path(r'^(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^$', permission_required(DashboardChartsView.as_view()), name='dashboard_charts'),
        re_path(r'^(?P<dashboard_configuration_id>\d+)/$', permission_required(DashboardDataView.as_view()), name='dashboard_data'),
        re_path(r'^settings/', include(settings_urlpatterns))
    ]))
]


