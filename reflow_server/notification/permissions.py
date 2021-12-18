from rest_framework import status

from reflow_server.notification.services.permissions import NotificationPermissionService
from reflow_server.core.permissions import PermissionsError


class NotificationDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, notification_configuration_id=None):
        self.notification_configuration_id = notification_configuration_id

    def __call__(self, request):
        if self.notification_configuration_id and \
            not NotificationPermissionService.is_valid(request.request.user, self.notification_configuration_id):
            raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)


class NotificationBillingPermission:
    def __init__(self, company_id):
        self.company_id = company_id

    def __call__(self, request):
        from reflow_server.notification.services.routes import notification_url_names
        if request.url_name in notification_url_names and request.method == 'POST':
            can_company_create_notification = NotificationPermissionService.validate_notification_creation(self.company_id, request.request.user.id)
            if not can_company_create_notification:
                raise PermissionsError(detail='invalid_billing', status=status.HTTP_403_FORBIDDEN)
