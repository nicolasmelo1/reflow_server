from reflow_server.notification.models import NotificationConfiguration, UserNotification, Notification

import math


class UserNotificationItem:
    def __init__(self, user_notifications, total_pages):
        self.user_notifications = user_notifications
        self.total_pages = total_pages
        

class NotificationService:
    @staticmethod
    def get_user_new_notifications_number(user_id):
        """
        Get new notifications number of user_id, so like if the user A has 20 new notifications (undread)
        it retrieve the number 20 for the user A. (notifications with is_new=True)

        Arguments:
            user_id {int} -- The id of the user you want to retrieve the number of notifications

        Returns:
            int -- Number of new notifications of the user.
        """
        user_read_notifications = UserNotification.objects.filter(
            user_id=user_id
        ).values_list('notification_id', flat=True)
        new_notifications = Notification.objects.filter(user_id=user_id, user__isnull=True).exclude(id__in=user_read_notifications)
        UserNotification.objects.bulk_create([UserNotification(notification=new_notification, user_id=user_id, is_new=True, has_read=False) for new_notification in new_notifications])
        return UserNotification.objects.filter(user_id=user_id, is_new=True).count()

    @staticmethod
    def get_and_update_user_notifications(user_id, page=1):
        """
        Retrive user_notifications and update them to is_new as False. This way when the user
        goes out of the notifications page, the user badge goes back to zero. (sets is_new to False)

        Arguments:
            user_id {int} -- the id of the user you want to retrieve notifications from

        Keyword Arguments:
            page {int} -- the current page of the notifications to retrieve, since the queryset 
                          is paginated we need the current page of the contents to retrieve (default: {1})

        Returns:
            UserNotificationItem -- simple object containing all of the queryset data and the total pages of the data
        """
        items_per_page = 25
        pagination_limit = items_per_page * page
        pagination_offset = pagination_limit - items_per_page
        user_notifications = UserNotification.objects.filter(user_id=user_id)
        user_notifications.update(is_new=False)
        user_notifications_response = UserNotificationItem(
            user_notifications.order_by('-created_at')[pagination_offset:pagination_limit], 
            math.ceil(user_notifications.count()/items_per_page)
        )
        return user_notifications_response
        
    @staticmethod
    def change_notification_field_names(old_field_name, new_field_name, company_id):
        """
        TODO: deprecate, we don't need it anymore
        """
        if old_field_name != new_field_name:
            for notification in  NotificationConfiguration.objects.filter(form__group__company_id=company_id, text__icontains='{{' + old_field_name + '}}'):
                notification.text = notification.text.replace('{{' + old_field_name + '}}', '{{' + new_field_name + '}}')
                notification.save()
    