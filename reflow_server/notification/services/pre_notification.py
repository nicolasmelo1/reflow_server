from django.conf import settings
from django.db.models import Q, Func, F, Value

from reflow_server.authentication.models import UserExtended
from reflow_server.data.models import FormValue
from reflow_server.notification.models import NotificationConfiguration, PreNotification
from reflow_server.data.services import DataService

from datetime import datetime, timedelta


class PreNotificationService:
    def update_from_request(self, company_id):
        """
        So this is the function to be called internally, it is used when we recieve a request from the worker that a notification
        configuration must be updated.

        We creates it this way so we can control the pre_notification creation inside of celery in our worker and without affecting
        the user request at all.

        Arguments:
            company_id {int} -- The company_id, we don't want to change EVERY notification, just the ones from the company.

        Keyword Arguments:
            user_id {int} -- the user_id, not obligatory (default: {None})
            dynamic_form_id {int} -- the dynamic_form_id, also not obligatory (default: {None})
            notification_configuration_id {int} -- the notification_configuration_id, not obligatory (default: {None})
        """
        self.__create_and_update_pre_notifications(company_id)

    @staticmethod
    def verify_pre_notifications():
        """
        Verify if has a pre_notification configuration to be fired now or less than now and fires the creation
        of the notification if it has.
        """
        now = datetime.now().replace(second=0, microsecond=0)
        pre_notifications = PreNotification.objects\
            .filter(has_sent=False, is_sending=False)\
            .annotate(truncated_when=Func(Value('minute'), F('when'), function='date_trunc'))\
            .filter(truncated_when__lte=now)
        if pre_notifications.exists():
            from reflow_server.notification.externals import NotificationWorkerExternal

            NotificationWorkerExternal().create_notification(pre_notifications.values_list('id', flat=True))
            pre_notifications.update(is_sending=True)

    @staticmethod
    def update(company_id):
        """
        This function is a simple function helper user to update the user`s pre_notification of a company. If the user_id, dynamic_form_id or notification_configuration_id
        has been changed, then you use this function to update the pre-notifications. 
        
        This function calls the worker so we can update it after the request is completed.

        > When the configurations of a user has changed, then he might not need to get
        a specific and particular notification.
        
        > When a formulary has changed, the date the notification is boud to might have changed also, so we need to update the notifications

        > If the user changed the notification_configuration, then you don't need to send it prior to 30 days, so it is 60 days now, so we need to update.

        We don't make it automatic, so everything that might change WHEN and for WHO the notification should be sent needs to be mapped and use this helper function.

        Arguments:
            company_id {int} -- The company_id, we don't want to change EVERY notification, just the ones from the company.
        """
        from reflow_server.notification.externals import NotificationWorkerExternal

        NotificationWorkerExternal().update_pre_notifications(company_id)

    def __create_and_update_pre_notifications(self, company_id):
        """
        This function is used to effectively create, update and delete pre_notifications.

        It's important to understand that we always update the notifications for all of the users of a company and all of the notifications
        that the users have access to.

        Why we gotta do it like this you might ask? The main problem is that we need to delete pre_notifications based on 3 
        conditions:
        
        - delete pre_notifications for users that are not from the same company as the notification (can happen if we are editing the db directly)
        - delete pre_notifications from formularies that is not meant to send notifications (the user can loose access to a certain form)
        - delete pre_notifications that the user has no access to (a user can loose access to a certain notification_configuration)

        As you might think, with this this function is not really optimized. :(
        So if you've got a better way to optimize it, please you can do it, but you gotta respect the conditions above.

        Arguments:
            company_id {int} -- The company id you want to update pre_notifications from
        """

        # if a form_id is defined we don't do anything much, just retrieve the forms data that the user has access to from the
        # form_id. Otherwise we retrieve ALL of the forms a user has access too and all of the forms data
        user_ids = UserExtended.objects.filter(company_id=company_id, is_active=True).values_list('id', flat=True)
        for user_id in user_ids:
            data_service = DataService(user_id, company_id)
            notification_configurations = NotificationConfiguration.objects.filter(Q(user_id=user_id) | Q(user__company_id=company_id, for_company=True))
            for notification_configuration in notification_configurations:
                form_data_accessed_by_user = data_service.get_user_form_data_ids_from_form_id(notification_configuration.form_id)
                self.__update_pre_notification(notification_configuration, user_id, form_data_accessed_by_user)
                
            # we usually create or update the pre_notifications in `.__update_pre_notification` function
            # but we usually don't delete the pre_notifications, that's why we need this part here.
            PreNotification.objects.filter(
                user_id=user_id, 
                has_sent=False
            ).exclude(
                notification_configuration__in=notification_configurations
            ).delete()

        
        PreNotification.objects.filter(
            notification_configuration__form__group__company_id=company_id, 
            has_sent=False
        ).exclude(
            user__company_id=company_id
        ).delete()

    
    def __update_pre_notification(self, notification_configuration, user_id, user_accessed_forms):
        """
        Filters and updates user PreNotifications based on FormValues values, this function is just a big query
        Might need rework for some improvements to be made.

        Arguments:
            notification_configuration {reflow_server.noticiation.models.NotificationConfiguration} -- the notification
            configuration to update the pre_notifications from
            user_id {int} -- the user_id to update the pre_notifications
            user_accessed_forms {list(int)} -- the form ids to update the pre_notifications
        """
        user = UserExtended.objects.filter(id=user_id).first()
        
        if notification_configuration.field.type.type in ['date']:
            form_values = FormValue.notification_.create_reminders_based_on_data_saved(
                user_accessed_forms, 
                notification_configuration.field,
                int(notification_configuration.days_diff),
                user.timezone
            )
            for  when, form_id in form_values:
                # force to just exist ONE pre_notification for this condition
                PreNotification.objects.filter(has_sent=False, user_id=user_id, dynamic_form_id=form_id, notification_configuration=notification_configuration).delete()
                PreNotification.objects.update_or_create(has_sent=False, user_id=user_id, dynamic_form_id=form_id, notification_configuration=notification_configuration, defaults={
                    'when':when
                })
            PreNotification.objects.filter(has_sent=False, user_id=user_id, notification_configuration=notification_configuration).exclude(dynamic_form_id__in=[form_id for _, form_id in form_values]).delete()
    