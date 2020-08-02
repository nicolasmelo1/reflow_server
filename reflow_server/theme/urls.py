from django.conf.urls import re_path, include
from django.conf import settings

from reflow_server.core.decorators import validate_billing
from reflow_server.theme.views import ThemeView, ThemeFormularyView, ThemeCompanyTypeView


urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/', include([
        re_path(r'^(?P<theme_id>\d+)/', include([
            re_path(r'^$', validate_billing(ThemeView.as_view()), name='theme_theme'),
            re_path(r'^(?P<theme_form_id>\d+)/$', validate_billing(ThemeFormularyView.as_view()), name='theme_formulary'), 
        ])),
        re_path(r'^company_type/(?P<company_type>\w+)/$', validate_billing(ThemeCompanyTypeView.as_view()), name='theme_company_type_themes')
    ]))
]