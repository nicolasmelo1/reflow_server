from django.conf.urls import re_path, include

from reflow_server.core.decorators import permission_required, authorize_external_response
from reflow_server.notification.views import NotificationConfigurationView, NotificationConfigurationEditView, NotificationConfigurationFieldsView, \
    UnreadAndReadNotificationView, NotificationsView, PreNotificationExternalView, NotificationConfigurationExternalView, VerifyPreNotificationExternalView


external_urlpatterns = [
    re_path(r'^build_notification/$', authorize_external_response(NotificationConfigurationExternalView.as_view()), name='notification_external_notification'),
    re_path(r'^pre_notification/', include([
        re_path(r'^$', authorize_external_response(VerifyPreNotificationExternalView.as_view()), name='notification_external_verify_pre_notification'),
        re_path(r'^(?P<company_id>\d+)/$', authorize_external_response(PreNotificationExternalView.as_view()), name='notification_external_pre_notification')
    ]))
]

settings_urlpatterns = [
    re_path(r'^$', permission_required(NotificationConfigurationView.as_view()), name='notification_notification_configuration'),
    re_path(r'^(?P<notification_configuration_id>\d+)/$', permission_required(NotificationConfigurationEditView.as_view()), name='notification_notification_configuration_edit'),
    re_path(r'^get_fields/(?P<form_id>\d+)/$', permission_required(NotificationConfigurationFieldsView.as_view()), name='notification_notification_configuration_fields'),
]

urlpatterns = [
    re_path(r'^external/', include(external_urlpatterns)),
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/', include([
        re_path(r'^$', permission_required(NotificationsView.as_view()), name='notification_load_data'),
        re_path(r'^read/$', permission_required(UnreadAndReadNotificationView.as_view()), name='notification_read_or_unread'),
        re_path(r'^settings/', include(settings_urlpatterns)),
    ])),
]