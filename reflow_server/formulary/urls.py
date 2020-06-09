from django.conf.urls import re_path, include

from reflow_server.core.decorators import permission_required, authorize_external_response
from reflow_server.formulary.views import GetFormularyView, GetGroupsView, UserFieldTypeOptionsView, \
    FormFieldTypeOptionsView


settings_urlpatterns = []


urlpatterns = [
    re_path(r'^(?P<company_id>\w+\.\w+)/', include([
        re_path(r'^settings/', include(settings_urlpatterns)),
        re_path(r'^$', permission_required(GetGroupsView.as_view()), name='formulary_get_groups'),
        re_path(r'^(?P<form>\w+)/', include([
            re_path(r'^$',permission_required(GetFormularyView.as_view()), name='formulary_get_formulary'),
            re_path(r'^(?P<field_id>)/user/options/$',permission_required(UserFieldTypeOptionsView.as_view()), name='formulary_get_user_field_type_options'),
            re_path(r'^(?P<field_id>)/form/options/$',permission_required(FormFieldTypeOptionsView.as_view()), name='formulary_get_form_field_type_options'),
        ]))
    ]))
]