from django.conf.urls import re_path, include

from reflow_server.authentication.services.routes import register_admin_only_url
from reflow_server.core.decorators import jwt_required, validate_billing, permission_required
from reflow_server.authentication.views import LoginView, TestTokenView, ForgotPasswordView, OnboardingView, \
    RefreshTokenView, ChangePasswordView, CompanyView, UserView, UserVisualizationTypeView
from reflow_server.authentication.views.settings import CompanySettingsView, UserSettingsView, UserSettingsEditView, \
    FormularyAndFieldOptionsView


settings_urlpatterns = [
    re_path(r'^(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/', include([
        re_path(r'^users/', include([
            re_path(r'^$', validate_billing(UserSettingsView.as_view()), name='authentication_settings_users'),
            re_path(r'^(?P<user_id>\d+)/$', validate_billing(UserSettingsEditView.as_view()), name='authentication_settings_edit_users'),
            re_path(r'^formulary_options/$', validate_billing(FormularyAndFieldOptionsView.as_view()), 
                name='authentication_settings_formulary_options'
            ),
        ])),
        re_path(r'^company/$', validate_billing(CompanySettingsView.as_view()), name='authentication_settings_company')
    ]))
]

loginrequired_urlpatterns = [
    register_admin_only_url(re_path(r'^settings/', include(settings_urlpatterns))),
    re_path(r'^test_token/$', jwt_required(TestTokenView.as_view()), name='authentication_test_token'),
    re_path(r'^(?P<company_id>(\w+(\.)?(-+)?(_)?)+)/', include([
        re_path(r'^user/', include([
            re_path(r'^$', permission_required(UserView.as_view()), name='authentication_user'),
            re_path(r'^visualization_type/(?P<visualization_type_id>\d+)/$', permission_required(UserVisualizationTypeView.as_view()), 
            name='authentication_user_set_visualization_type_id')
        ])),
        re_path(r'^company/$', permission_required(CompanyView.as_view()), name='authentication_company')

    ]))
]

urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='authentication_login'),
    re_path(r'^forgot/$', ForgotPasswordView.as_view(), name='authentication_forgot_password'),
    re_path(r'^onboarding/$', OnboardingView.as_view(), name='authentication_onboarding'),
    re_path(r'^refresh_token/$', RefreshTokenView.as_view(), name='authentication_refresh_token'),
    re_path(r'^change_password/$', ChangePasswordView.as_view(), name='authentication_change_password')
] + loginrequired_urlpatterns