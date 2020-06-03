from django.conf.urls import re_path

from reflow_server.core.decorators import jwt_required
from reflow_server.authentication.views import LoginView, TestTokenView, ForgotPasswordView, OnboardingView, \
    RefreshTokenView, ChangePasswordView

loginrequired_urlpatterns = [
    re_path(r'^test_token/$', jwt_required(TestTokenView.as_view()), name='authentication_test_token'),
]

urlpatterns = [
    re_path(r'^login/$', LoginView.as_view(), name='authentication_login'),
    re_path(r'^forgot/$', ForgotPasswordView.as_view(), name='authentication_forgot_password'),
    re_path(r'^onboarding/$', OnboardingView.as_view(), name='authentication_onboarding'),
    re_path(r'^refresh_token/$', RefreshTokenView.as_view(), name='authentication_refresh_token'),
    re_path(r'^change_password/$', ChangePasswordView.as_view(), name='authentication_change_password')
] + loginrequired_urlpatterns