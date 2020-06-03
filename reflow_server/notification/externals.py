from django.conf import settings

from reflow_server.notification.serializers import PreNotificationSerializer
from reflow_server.core import externals


class NotificationWorkerExternal(externals.External):
    host = settings.EXTERNAL_APPS['reflow_worker'][0]

    def create_notification(self, pre_notifications_list_ids):
        """
        Works like a bridge, we send a request to reflow worker, the reflow worker doesn't do anything
        with the data, and use this data sending it back to NotificationConfigurationExternalView.post request.

        This view handles the retrieval of the data needed to build the notifications.
        """
        self.post('/notification/', data=list(pre_notifications_list_ids))

    def update_pre_notifications(self, company_id):
        data = {
            'user_id': None,
            'dynamic_form_id': None,
            'notification_configuration_id': None
        }
        serializer = PreNotificationSerializer(data=data)
        serializer.is_valid()
        self.post('/notification/pre_notification/{}/'.format(company_id), serializer.data)
        