from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.pdf_generator.views import PDFTemplateConfigurationView, PDFTemplatesFieldOptionsView, \
    PDFTemplateConfigurationEditView

settings_urlpatterns = [
    re_path(r'^$', validate_billing(PDFTemplateConfigurationView.as_view()), name='pdf_generator_template_configuration'),
    re_path(r'^(?P<pdf_template_configuration_id>\d+)/$', validate_billing(PDFTemplateConfigurationEditView.as_view()), name='pdf_generator_template_configuration_edit'),
    re_path(r'^field_options/$', validate_billing(PDFTemplatesFieldOptionsView.as_view()), name='pdf_generator_configuration_field_options')
]

urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^settings/', include(settings_urlpatterns)),
    ]))
] 