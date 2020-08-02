from django.conf.urls import re_path, include

from reflow_server.core.utils.routes import register_dashbaord_settings_url
from reflow_server.core.decorators import validate_billing
from reflow_server.dashboard.views import DashboardChartConfigurationView, DashboardChartConfigurationEditView, \
    DashboardFieldsView, DashboardChartsView, DashboardDataView

settings_urlpatterns = [
    register_dashbaord_settings_url(re_path(r'^$', validate_billing(DashboardChartConfigurationView.as_view()), name='dashboard_chart_configuration')),
    register_dashbaord_settings_url(re_path(r'^(?P<dashboard_configuration_id>\d+)/$', validate_billing(DashboardChartConfigurationEditView.as_view()), name='dashboard_chart_edit_configuration')),
    re_path(r'^field_options/$', validate_billing(DashboardFieldsView.as_view()), name='dashboard_fields_configuration')
]

urlpatterns = [
    re_path(r'^(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^$', validate_billing(DashboardChartsView.as_view()), name='dashboard_charts'),
        re_path(r'^(?P<dashboard_configuration_id>\d+)/$', validate_billing(DashboardDataView.as_view()), name='dashboard_data'),
        re_path(r'^settings/', include(settings_urlpatterns))
    ]))
]


