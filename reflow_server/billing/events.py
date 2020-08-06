from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from reflow_server.authentication.models import UserExtended


class BillingEvents:
    """
    This class is used for sending real time events for the client about this service
    """
    @staticmethod 
    def send_updated_billing(company_id):
        """
        This event sends to all of the clients of the company that
        the company they are in have updated its billing information.

        Arguments:
            company_id {int} -- What company was the formulary
        """
        channel_layer = get_channel_layer()

        for user in UserExtended.objects.filter(company_id=company_id, is_active=True):
            group_name = 'user_{}'.format(user.id)
            async_to_sync(channel_layer.group_send)(
                '{}'.format(group_name),
                {
                    'type': 'send_billing_was_updated',
                    'data': {
                        'company_id': company_id
                    }
                }
            )