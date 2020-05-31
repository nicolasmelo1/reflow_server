from django.conf import settings
from django.db.models import Q, Func, F, Value, ExpressionWrapper, DateTimeField

from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.models import FormAccessedBy, FormValue, DynamicForm, OptionAccessedBy
from reflow_server.notification.models import NotificationConfiguration, PreNotification
from reflow_server.formulary.services.data import DataService

from datetime import datetime, timedelta


class PreNotificationService:
    @staticmethod
    def update(company_id, user_id=None, dynamic_form_id=None, notification_configuration_id=None):
        """
        This function is a simple function helper user to update the user`s pre_notification of a company. If the user_id, dynamic_form_id or notification_configuration_id
        has been changed, then you use this function to update the pre-notifications. 
        
        > When the configurations of a user has changed, then he might not need to get
        a specific and particular notification.
        
        > When a formulary has changed, the date the notification is boud to might have changed also, so we need to update the notifications

        > If the user changed the notification_configuration, then you don't need to send it prior to 30 days, so it is 60 days now, so we need to update.

        We don't make it automatic, so everything that might change WHEN and for WHO the notification should be sent needs to be mapped and use this helper function.

        Arguments:
            company_id {int} -- The company_id, we don't want to change EVERY notification, just the ones from the company.

        Keyword Arguments:
            user_id {int} -- the user_id, not obligatory (default: {None})
            dynamic_form_id {int} -- the dynamic_form_id, also not obligatory (default: {None})
            notification_configuration_id {int} -- the notification_configuration_id, not obligatory (default: {None})
        """
        pre_notification_service = PreNotificationService()
        if user_id:
            pre_notification_service.create_and_update_user_pre_notifications(user_id, company_id)
        if notification_configuration_id:
            pre_notification_service.create_and_update_notification_configuration_pre_notifications(notification_configuration_id, company_id)
        if dynamic_form_id:
            pre_notification_service.create_and_update_form_pre_notifications(dynamic_form_id, company_id)

    def __create_and_update_pre_notifications(self, company_id, user_id, form_names_accessed_by_user, form_id=None, notification_configuration=None):
        """
        This function is used to effectively create or update pre_notifications based on certain conditions.
        If it recieved a user_id, it updates all of the pre_notifications of the formularies that the user has access to.

        So instead of updating each individual pre_notification on user, or notification_configuration level. We always try to
        update them on form data level. So if a user has changed, we get all the form data that this user has access to to update.
        If a change in the notification_configuration is made we get all of the form data that this notification configuration
        complies to. 

        I understand this is kinda tricky, but this is why we need 3 different handler methods `.create_and_update_user_pre_notifications()`,
        `.create_and_update_notification_configuration_pre_notifications()` and `.create_and_update_form_pre_notifications()` for each condition.
        The outcome of all of them is ALWAYS the same. We always update based from the user_id

        Arguments:
            company_id {int} -- The company id you want to update pre_notifications from
            user_id {int} -- you always need to update pre_notifcations for a certain user. It's never for the hole company.

        Keyword Arguments:
            form_id {int} -- Only required if you want to update the pre_notifications from a certain
                             form data. (default: {None})
            notification_configuration {reflow_server.notification.models.NotificationConfiguration} -- 
            Only required if you want to update the pre_notifcations of a certain notification_configuration (default: {None})
        """

        # if a form_id is defined we don't do anything much, just retrieve the forms data that the user has access to from the
        # form_id. Otherwise we retrieve ALL of the forms a user has access too and all of the forms data
        data_service = DataService(user_id, company_id)

        if form_id:
            user_accessed_forms = data_service.get_user_form_data_ids_from_form_id(form_id).values_list('id', flat=True)
        else:
            user_accessed_forms = data_service.all_form_data_a_user_has_access_to()

        # checks if it's a single notification_configuration or update multiple notification configurations
        if notification_configuration:
            self.__update_pre_notification(notification_configuration, user_id, user_accessed_forms)
        else:
            # check if needs to change all notification_configurations or only the ones from a form_id
            if form_id:
                notification_configurations = NotificationConfiguration.objects.filter(form_id=form_id)
            else:
                # this is used if you are trying to change the pre_notifications of a user. since the user can have his own notifications
                # we first need to check his own notification_configurations, on the other hand, admins can set notifications for the hole
                # company, company which the user can be part of. So we have 2 distinct conditions: his own notification_configurations and
                # his company notification_configurations. 
                notification_configurations = NotificationConfiguration.objects.filter(Q(user_id=user_id) | Q(user__company_id=company_id, for_company=True))
            for notification_configuration in notification_configurations:
                self.__update_pre_notification(notification_configuration, user_id, user_accessed_forms)

        # we usually create or update the pre_notifications in `.__update_pre_notification` function
        # but we usually don't delete the pre_notifications, that's why we need this part here.
        PreNotification.objects.filter(user_id=user_id, has_sent=False).exclude(dynamic_form_id__in=user_accessed_forms).delete()
    
    
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
            # it is important to notice that on the second annotate we convert the value to the same date as the server
            # so when we filter, we already got the server time so no need to add or subtract timedelta
            form_values = FormValue.objects.filter(form__depends_on_id__in=user_accessed_forms, field=notification_configuration.field, field_type__type='date')\
                                           .annotate(value_as_date=Func(F('value'), Value(settings.DEFAULT_PSQL_DATE_FIELD_FORMAT), function='to_timestamp'))\
                                           .annotate(value_as_date=ExpressionWrapper(F('value_as_date') + timedelta(days=int(notification_configuration.days_diff)) - timedelta(hours=user.timezone), output_field=DateTimeField()))\
                                           .filter(value_as_date__gte=datetime.now())\
                                           .values_list('value_as_date','form__depends_on_id')
            for  when, form_id in form_values:
                PreNotification.objects.update_or_create(has_sent=False, user_id=user_id, dynamic_form_id=form_id, notification_configuration=notification_configuration, defaults={
                    'when':when
                })
        
    def create_and_update_user_pre_notifications(self, user_id, company_id):
        """
        Used to update pre_notifications of a user_id. Usually used when a user_id is updated or created

        Arguments:
            user_id {int} -- The user_id to update
            company_id {int} -- the company_id that the user resides on to update
        """
        self.__create_and_update_pre_notifications(company_id=company_id, user_id=user_id)

    def create_and_update_notification_configuration_pre_notifications(self, notification_configuration_id, company_id):
        """
        Used to update the pre_notifications of a notification_configuration, usually used when a notification_configuration
        is updated or created.

        Arguments:
            notification_configuration_id {int} -- the id of the notification_configuration that was created or updated
            company_id {int} -- the id of the company that the notification_configuration resides on
        """
        notification_configuration = NotificationConfiguration.objects.filter(id=notification_configuration_id).first()
        # updates single user or multiple users for a certain company
        if notification_configuration.for_company:
            user_ids = UserExtended.objects.filter(company_id=company_id, is_active=True).values_list('id', flat=True)
            for user_id in user_ids:
                
                self.__create_and_update_pre_notifications(company_id=company_id, user_id=user_id, notification_configuration=notification_configuration)
        else:
            self.__create_and_update_pre_notifications(company_id=company_id, user_id=notification_configuration.user_id, notification_configuration=notification_configuration)

    def create_and_update_form_pre_notifications(self, dynamic_form_id, company_id):
        """
        Used to update the pre_notifications of a form data id, so if a formulary has been created or updated, we need to also update
        the pre_notification that resides on the form_id

        Arguments:
            dynamic_form_id {int} -- The form data id that was created or updated
            company_id {int} -- the company_id that the form_data id resides on.
        """
        dynamic_form = DynamicForm.objects.filter(id=dynamic_form_id, depends_on__isnull=True).first()
        if dynamic_form:
            form_id = dynamic_form.form_id
            form_values = FormValue.objects.filter(form__depends_on=dynamic_form, field__type__type__in=['option','multi_option'])
            user_ids = FormAccessedBy.objects.filter(form=dynamic_form.form, user__company_id=company_id, user__is_active=True).values_list('user_id', flat=True)
            for form_value in form_values:
                user_ids = OptionAccessedBy.objects.filter(user_id__in=user_ids, field_option__field=form_value.field, field_option__option=form_value.value).values_list('user_id', flat=True)

            for user_id in user_ids:
                self.__create_and_update_pre_notifications(company_id=company_id, user_id=user_id, form_id=form_id)

