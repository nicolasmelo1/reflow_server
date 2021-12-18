from reflow_server.notification.models import NotificationConfiguration
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.billing.services import BillingService


class NotificationPermissionService:
    """
    Used for validating the notification permissions.
    """
    @staticmethod
    def is_valid(user, notification_configuration_id):
        return NotificationConfiguration.objects.filter(user=user, id=notification_configuration_id).exists()

    @staticmethod
    def validate_notification_creation(company_id, user_id):
        number_of_notifications = NotificationConfiguration.notification_.number_of_notifications_by_user_and_company(company_id, user_id)
        current_notifications_permission_for_company = CurrentCompanyCharge.notification_.quantity_of_permitted_notifications_for_company_id(company_id)
        if number_of_notifications + 1 >= current_notifications_permission_for_company:
            return False
        else:
            return True