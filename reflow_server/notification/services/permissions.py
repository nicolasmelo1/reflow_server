from reflow_server.notification.models import NotificationConfiguration


class NotificationPermissionService:
    """
    Used for validating the notification permissions.
    """
    @staticmethod
    def is_valid(user, notification_configuration_id):
        return NotificationConfiguration.objects.filter(user=user, id=notification_configuration_id).exists()
