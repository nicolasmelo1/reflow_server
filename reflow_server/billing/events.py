from reflow_server.authentication.models import UserExtended
from reflow_server.core.utils.channel_layers import ChannelLayer


class BillingBroadcastEvent:
    """
    This class is used for sending real time events for the client about this domain
    """
    def new_paying_company(self, user_id, company_id, total_paying_value):
        """
        This event sends to all of the clients of the company that
        the company they are in have updated its billing information.

        Args:
            user_id (int): A UserExtended instance id of the user that edited the payment information
            company_id (int): What company was the formulary
            total_paying_value (float): How much reflow will charge for the company at the current time
        """
        for user in UserExtended.billing_.users_active_by_company_id(company_id):
            group_name = 'user_{}'.format(user.id)
            ChannelLayer.broadcast_to_group(group_name, 'send_billing_was_updated', {
                'is_new_paying_company': True,
                'company_id': company_id,
                'user_id': user_id
            })
    
    def updated_billing_information(self, user_id, company_id, total_paying_value):
        """
        This is similar to 'new_paying_company' event, except this event is fired whenever the billing information
        was updated, in other words, when the company is a paying company but adds a new user or just change the billing information
        like address and so on.

        Args:
            user_id (int): A UserExtended instance id of the user that edited the payment information
            company_id (int): What company was the formulary
            total_paying_value (float): How much reflow will charge for the company at the current time
        """
        for user in UserExtended.billing_.users_active_by_company_id(company_id):
            group_name = 'user_{}'.format(user.id)
            ChannelLayer.broadcast_to_group(group_name, 'send_billing_was_updated', {
                'is_new_paying_company': True,
                'company_id': company_id,
                'user_id': user_id
            })