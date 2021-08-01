from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync


class ChannelLayer:
    """
    A simple helper class responsible for dealing with channel layers:

    Right now it only broadcast a message to groups

    Reference: https://channels.readthedocs.io/en/stable/topics/channel_layers.html
    """
    @staticmethod
    def broadcast_to_group(group_name, message_type, data={}):
        """
        Broadcast a message to a group.

        Args:
            group_name (str): The name of the group you want to send the message to.
            message_type (str): The 'type' part of the message, this is obrigatory.
            data (dict): The data you want to send to the user.
        """
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            '{}'.format(group_name),
            {
                'type': message_type,
                'data': data
            }
        )

