from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.pdf_generator.services.routes import register_pdf_generator_generate_url_name
from reflow_server.pdf_generator.views import PDFTemplateConfigurationView, PDFTemplatesFieldOptionsView, \
    PDFTemplateConfigurationEditView, PDFTemplatesValuesOptionsView, PDFTemplatesForReaderView, PDFGenerateView, \
    PDFTemplateAllowedTextBlockView, PDFTemplateGetDataForReaderView

settings_urlpatterns = [
    re_path(r'^$', validate_billing(PDFTemplateConfigurationView.as_view()), name='pdf_generator_template_configuration'),
    re_path(r'^(?P<pdf_template_configuration_id>\d+)/$', validate_billing(PDFTemplateConfigurationEditView.as_view()), name='pdf_generator_template_configuration_edit'),
    re_path(r'^field_options/$', validate_billing(PDFTemplatesFieldOptionsView.as_view()), name='pdf_generator_configuration_field_options')
]

urlpatterns = [
    re_path(r'allowed_blocks/$', validate_billing(PDFTemplateAllowedTextBlockView.as_view()), name='pdf_generator_allowed_blocks'),
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^$', validate_billing(PDFTemplatesForReaderView.as_view()), name='pdf_generator_reader_templates'),
        re_path(r'^(?P<pdf_template_configuration_id>\d+)/', include([
            re_path(r'^$', validate_billing(PDFTemplateGetDataForReaderView.as_view()), name='pdf_generator_reader_get_single_template'),
            re_path(r'^value_options/(?P<dynamic_form_id>\d+)/$', validate_billing(PDFTemplatesValuesOptionsView.as_view()), name='pdf_generator_reader_value_options'),
            register_pdf_generator_generate_url_name(
                re_path(r'^generate/$', validate_billing(PDFGenerateView.as_view()), name='pdf_generator_generate')
            ),
        ])),
        re_path(r'^settings/', include(settings_urlpatterns)),
    ]))
] 