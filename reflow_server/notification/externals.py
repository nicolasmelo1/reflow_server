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
        from reflow_server.notification.serializers import PreNotificationIdsForBuildSerializer

        data = {
            'pre_notification_ids': list(pre_notifications_list_ids)
        }
        serializer = PreNotificationIdsForBuildSerializer(data=data)
        self.post('/notification/external/build_notification/', data=serializer.initial_data)

    def update_pre_notifications(self, company_id):
        """
        This is used to update pre_notifications, we send this to the worker application
        so the worker calls this application again sending back the data. This way we don't
        stop the user from saving a notification_configuration instance, saving a user instance
        or a DynamicForm instance. We resolve the pre_notification after the
        data have been saved.

        Args:
            company_id (int): The reflow_server.authentication.models.Company instance id
        """
        data = {
            'user_id': None,
            'dynamic_form_id': None,
            'notification_configuration_id': None
        }
        serializer = PreNotificationSerializer(data=data)
        serializer.is_valid()
        self.post('/notification/external/pre_notification/{}/'.format(company_id), serializer.data)
        