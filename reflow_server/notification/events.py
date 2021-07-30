from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from reflow_server.authentication.models import UserExtended


class NotificationEvents:
    """
    This is using for sending real time events for the client
    """
    @staticmethod 
    def send_notification_number(user_id):
        """
        This event sends a new notification number to the connected client

        Arguments:
            user_id {int} -- for what user you want to send this event
        """
        channel_layer = get_channel_layer()
        group_name = 'user_{}'.format(user_id)
        async_to_sync(channel_layer.group_send)(
            '{}'.format(group_name),
            {
                'type': 'send_notification'
            }
        )
