from django.conf.urls import re_path, include

from reflow_server.automation.views import AutomationWebhookVersion1View, AutomationSettingsAppsView, \
    AutomationSettingsInputFormularyView


settings_urlpatterns = [
    re_path(r'^$', AutomationSettingsAppsView.as_view(), name='automation_settings_apps_view'),
    re_path(r'^input_formulary/(?P<input_formulary_id>\d+)/$', AutomationSettingsInputFormularyView.as_view(), name='automation_settings_input_formulary_view')
]

urlpatterns = [
    re_path(r'^webhook/v1/(?P<app_name>\w+)/(?P<automation_trigger_name>\w+)/(?P<user_id>\d+)/$', AutomationWebhookVersion1View.as_view(), name='automation_v1_webhook'),
    re_path(r'^(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/', include([
        re_path(r'^settings/', include(settings_urlpatterns))
    ]))
]