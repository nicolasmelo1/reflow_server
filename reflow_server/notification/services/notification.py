from django.db import transaction
from django.db.models import Q

from reflow_server.notification.models import NotificationConfiguration, UserNotification, Notification, PreNotification
from reflow_server.notify.services import NotifyService

import math


class UserNotificationResponse:
    def __init__(self, user_notifications, total_pages):
        """
        Simple class that contains all of the queryset data and the total pages of the data

        Arguments:
            user_notifications {Queryset(reflow_server.notification.models.UserNotification)} -- The queryset containing
                                                                                                 all of the notifications
                                                                                                 of a user.
            total_pages {int} -- An interger that represents all of the pages to retrieve user notifications
        """
        self.user_notifications = user_notifications
        self.total_pages = total_pages
        

class NotificationService:
    def __init__(self):
        self.__notifications = list()
        self.__pre_notification_ids = list()

    def add_notification(self, pre_notification_id, notification_text, notification_configuration_id, dynamic_form_id, user_id):
        """
        Method used for appending each Notification object model to a list so we can bulk create the notifications
        This method is also responsible for appending pre_notification_ids to a list so we can update the objects.

        Arguments:
            pre_notification_id {int} -- the id of the pre_notification that created this notification.
            notification_text {str} -- The notification text
            notification_configuration_id {int} -- the notification configuration id
            form_id {int} -- the form data id for which form data this notification references to
            user_id {int} -- the user id to know for which user this notification references to
        """
        self.__pre_notification_ids.append(pre_notification_id)
        self.__notifications.append(
            Notification(
                notification=notification_text, 
                notification_configuration_id=notification_configuration_id, 
                form_id=dynamic_form_id, 
                user_id=user_id
            )
        )

    @transaction.atomic
    def create_notifications(self):
        """
        Must be called after calling `.add_notification()` to add your notifications
        """
        if not self.__notifications or not self.__pre_notification_ids:
            raise AssertionError('You must call `.add_notification()` method before calling `.create_notification()` method')
        
        PreNotification.objects.filter(id__in=self.__pre_notification_ids, has_sent=False, is_sending=True).update(has_sent=True, is_sending=False)
        created_notifications = Notification.objects.bulk_create(self.__notifications)
        NotifyService.send_new_notifications(self.__notifications)
        return created_notifications

    @staticmethod
    def get_user_new_notifications_number(user_id, company_id):
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
        new_notifications = Notification.objects.filter(
            Q(user_id=user_id) | 
            Q(user__isnull=True, notification_configuration__for_company=True, form__company_id=company_id)
        ).exclude(
            id__in=user_read_notifications
        )
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
            UserNotificationResponse -- simple object containing all of the queryset data and the total pages of the data
        """
        items_per_page = 25
        pagination_limit = items_per_page * page
        pagination_offset = pagination_limit - items_per_page
        user_notifications = UserNotification.objects.filter(user_id=user_id)
        user_notifications.update(is_new=False)
        user_notifications_response = UserNotificationResponse(
            user_notifications.order_by('-notification__created_at')[pagination_offset:pagination_limit], 
            math.ceil(user_notifications.count()/items_per_page)
        )
        return user_notifications_response
    