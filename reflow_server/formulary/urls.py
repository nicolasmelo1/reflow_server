from django.conf.urls import re_path, include

from reflow_server.core.utils.routes import register_admin_only_url
from reflow_server.core.decorators import permission_required, authorize_external_response
from reflow_server.formulary.views import GetFormularyView, GetGroupsView, UserFieldTypeOptionsView, \
    FormFieldTypeOptionsView
from reflow_server.formulary.views.settings import GroupSettingsView, GroupEditSettingsView, FormularySettingsView, \
    FormularySettingsEditView, SectionSettingsView, SectionSettingsEditView, FieldSettingsView, FieldSettingsEditView

settings_urlpatterns = [
    re_path(r'^groups/', include([
        re_path(r'^$', permission_required(GroupSettingsView.as_view()), name='formulary_settings_groups'),
        re_path(r'^(?P<group_id>\d+)/$', permission_required(GroupEditSettingsView.as_view()), name='formulary_settings_edit_groups')
    ])),
    re_path(r'^forms/', include([
        re_path(r'^$', permission_required(FormularySettingsView.as_view()), name='formulary_settings_forms'),
        re_path(r'^(?P<form_id>\d+)/$', permission_required(FormularySettingsEditView.as_view()), name='formulary_settings_edit_forms')
    ])),
    re_path(r'^sections/(?P<form_id>\d+)/', include([
        re_path(r'^$', permission_required(SectionSettingsView.as_view()), name='formulary_settings_sections'),
        re_path(r'^(?P<section_id>\d+)/$', permission_required(SectionSettingsEditView.as_view()), name='formulary_settings_edit_sections') 
    ])),
    re_path(r'^fields/(?P<form_id>\d+)/', include([
        re_path(r'^$', permission_required(FieldSettingsView.as_view()), name='formulary_settings_fields'),
        re_path(r'^(?P<field_id>\d+)/$', permission_required(FieldSettingsEditView.as_view()), name='formulary_settings_edit_fields')
    ]))
]


urlpatterns = [
    re_path(r'^(?P<company_id>\w+\.\w+)/', include([
        register_admin_only_url(re_path(r'^settings/', include(settings_urlpatterns))),
        re_path(r'^$', permission_required(GetGroupsView.as_view()), name='formulary_get_groups'),
        re_path(r'^(?P<form>\w+)/', include([
            re_path(r'^$',permission_required(GetFormularyView.as_view()), name='formulary_get_formulary'),
            re_path(r'^(?P<field_id>)/user/options/$',permission_required(UserFieldTypeOptionsView.as_view()), name='formulary_get_user_field_type_options'),
            re_path(r'^(?P<field_id>)/form/options/$',permission_required(FormFieldTypeOptionsView.as_view()), name='formulary_get_form_field_type_options'),
        ]))
    ]))
]