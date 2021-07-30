from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from reflow_server.authentication.models import UserExtended


class FormularyEvents:
    """
    This class is used for sending real time events about Formularies
    """
    @staticmethod 
    def send_updated_formulary(company_id, form_id, form_name):
        """
        This event sends to all of the clients of a company that a formulary have been updated

        Arguments:
            company_id {int} -- What company updated the formulary
            form_id {int} -- the id of the formulary/page updated
            form_name {str} --  The name of the updated formulary
        """
        channel_layer = get_channel_layer()

        for user in UserExtended.data_.users_active_by_company_id(company_id):
            group_name = 'user_{}'.format(user.id)
            async_to_sync(channel_layer.group_send)(
                '{}'.format(group_name),
                {
                    'type': 'send_formulary_created_or_updated',
                    'data': {
                        'form_name': form_name,
                        'form_id': form_id,
                        'company_id': company_id
                    }
                }
            )