from reflow_server.core.utils.channel_layers import ChannelLayer
from reflow_server.authentication.models import UserExtended


class AuthenticationBroadcastEvent:
    """
    This class is used for sending real time events for the client about this domain
    """
    def company_information_updated(self, user_id, company_id):
        """
        This event sends to all of the clients of the company that
        the company they are in have updated its company information.

        Args:
            user_id (int): The UserExtended instance id of the user that had updated the company information
            company_id (int): The company_id that was updated
        """
        for user in UserExtended.authentication_.users_active_by_company_id(company_id):
            group_name = 'user_{}'.format(user.id)
            ChannelLayer.broadcast_to_group(group_name, 'send_company_was_updated', {
                'user_id': user_id,
                'company_id': company_id
            })
            