from django.conf.urls import re_path, include
from django.conf import settings

from reflow_server.core.decorators import validate_billing
from reflow_server.theme.views import ThemeView, ThemeFormularyView, ThemeThemeTypeView, SelectThemeView
from reflow_server.theme.views.settings import ThemeSettingsView


settings_urlpatterns = [
    re_path(r'^$', validate_billing(ThemeSettingsView.as_view()), name='theme_settings_view')
]


urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/', include([
        re_path(r'^settings/', include(settings_urlpatterns)),
        re_path(r'^(?P<theme_id>\d+)/', include([
            re_path(r'^$', validate_billing(ThemeView.as_view()), name='theme_theme'),
            re_path(r'^select/$', validate_billing(SelectThemeView.as_view()), name='theme_select'),
            re_path(r'^(?P<theme_form_id>\d+)/$', validate_billing(ThemeFormularyView.as_view()), name='theme_formulary'), 
        ])),
        re_path(r'^theme_type/(?P<theme_type_id>\w+)/$', validate_billing(ThemeThemeTypeView.as_view()), name='theme_theme_type_themes'),
    ]))
]