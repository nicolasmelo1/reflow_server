from django.conf.urls import re_path, include

from reflow_server.authentication.services.routes import register_admin_only_url, register_can_be_public_url
from reflow_server.core.decorators import validate_billing
from reflow_server.authentication.decorators import get_company_id_as_int
from reflow_server.formulary.views import GetFormularyView, GetGroupsView, UserFieldTypeOptionsView, \
    FormFieldTypeOptionsView, PublicFormularyDataView
from reflow_server.formulary.views.settings import GroupSettingsView, GroupEditSettingsView, FormularySettingsView, \
    FormularySettingsEditView, SectionSettingsView, SectionSettingsEditView, FieldSettingsView, FieldSettingsEditView, \
    FieldOptionsView, PublicFormSettingsView, DefaultValueAttachmentView


settings_urlpatterns = [
    re_path(r'(?P<form_id>\d+)/public/$', validate_billing(PublicFormSettingsView.as_view()), name='formulary_public_form_settings'),
    re_path(r'(?P<form_id>\d+)/field_options/$', validate_billing(FieldOptionsView.as_view()), name='formulary_field_options'),
    re_path(r'^groups/', include([
        re_path(r'^$', validate_billing(GroupSettingsView.as_view()), name='formulary_settings_groups'),
        re_path(r'^(?P<group_id>\d+)/$', validate_billing(GroupEditSettingsView.as_view()), name='formulary_settings_edit_groups')
    ])),
    re_path(r'^forms/', include([
        re_path(r'^$', validate_billing(FormularySettingsView.as_view()), name='formulary_settings_forms'),
        re_path(r'^(?P<form_id>\d+)/$', validate_billing(FormularySettingsEditView.as_view()), name='formulary_settings_edit_forms')
    ])),
    re_path(r'^sections/(?P<form_id>\d+)/', include([
        re_path(r'^$', validate_billing(SectionSettingsView.as_view()), name='formulary_settings_sections'),
        re_path(r'^(?P<section_id>\d+)/$', validate_billing(SectionSettingsEditView.as_view()), name='formulary_settings_edit_sections') 
    ])),
    re_path(r'^fields/(?P<form_id>\d+)/', include([
        re_path(r'^$', validate_billing(FieldSettingsView.as_view()), name='formulary_settings_fields'),
        re_path(r'^(?P<field_id>\d+)/defaults/(?P<file_name>.+)/$', validate_billing(DefaultValueAttachmentView.as_view()), name='formulary_settings_default_value_attachment_view'),
        re_path(r'^(?P<field_id>\d+)/$', validate_billing(FieldSettingsEditView.as_view()), name='formulary_settings_edit_fields')
    ]))
]


urlpatterns = [
    re_path(r'^(?P<company_id>(\w+(\.)?(-)?(_)?)+)/', include([
        register_admin_only_url(re_path(r'^settings/', include(settings_urlpatterns))),
        re_path(r'^$', validate_billing(GetGroupsView.as_view()), name='formulary_get_groups'),
        register_can_be_public_url(
            re_path(r'^(?P<form>\w+)/', include([
                re_path(r'^$',validate_billing(GetFormularyView.as_view()), name='formulary_get_formulary'),
                re_path(r'^(?P<field_id>\d+)/user/options/$',validate_billing(UserFieldTypeOptionsView.as_view()), name='formulary_get_user_field_type_options'),
                re_path(r'^(?P<field_id>\d+)/form/options/$',validate_billing(FormFieldTypeOptionsView.as_view()), name='formulary_get_form_field_type_options'),
            ]))
        )
    ])),
    re_path(r'^public/(?P<company_id>(\w+(\.)?(-)?(_)?)+)/form/(?P<form>\w+)/$', get_company_id_as_int(PublicFormularyDataView.as_view()), name='public_formulary_data_view')
]