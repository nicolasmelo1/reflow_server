from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from reflow_server.authentication.models import UserExtended


class AuthenticationEvents:
    """
    This class is used for sending real time events for the client about this domain
    """
    @staticmethod
    def send_updated_company(company_id):
        """
        This event sends to all of the clients of the company that
        the company they are in have updated its company information.

        Args:
            company_id (int): The company_id that was updated
        """
        channel_layer = get_channel_layer()

        for user in UserExtended.authentication_.users_active_by_company_id(company_id):
            group_name = 'user_{}'.format(user.id)
            async_to_sync(channel_layer.group_send)(
                '{}'.format(group_name),
                {
                    'type': 'send_company_was_updated',
                    'data': {
                        'company_id': company_id
                    }
                }
            )
