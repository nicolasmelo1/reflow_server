from reflow_server.notify.models import PushNotification


class PushService:
    def __init__(self, user_id, title_variables=[], body_variables=[]):
        """
        This service is used to create each push notification data individually for each recipient and also send the push
        notification to a group of users.

        Args:
            user_id (int): The id of the user you want to send push notification to
            title_variables (list, optional): The variables of the title on the push notifications. Defaults to list().
            body_variables (list, optional): The variables of the body on the push notifications. Defaults to list().
        """
        self.title_variables = title_variables
        self.body_variables = body_variables
        self.tokens = list(PushNotification.objects.filter(user_id=user_id).values('token', 'push_notification_tag_type__name'))
        self.variables = variables

    @staticmethod
    def add_variable(variable_name, variable_value):
        return {
            'name': variable_name,
            'value': variable_value
        }

    @staticmethod
    def send_push(template_name, pushs):
        """
        Handy function to forward push notifications to reflow_worker so reflow_worker can take care of 
        the push notification sending.

        Arguments:
            template_name {str} -- name of the push notification template in reflow_worker
            pushs {list(Push)} -- List of Push objects
        """
        from reflow_server.notify.externals import PusherExternal

        PusherExternal().send_mail(template_name, pushs)