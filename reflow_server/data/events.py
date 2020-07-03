from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from reflow_server.authentication.models import UserExtended


class DataEvents:
    """
    This class is used for sending real time events for the client about this service
    """
    @staticmethod 
    def send_updated_formulary(company_id, dynamic_form_id, form_id, updated_user_id):
        """
        This event sends to all of the clients of a company that a formulary have been updated

        Arguments:
            company_id {int} -- What company updated the formulary
            dynamic_form_id {int} -- the id of the formulary data added or updated
            form_id {int} -- the id of the formulary/page updated
            updated_user_id {int} -- what user id updated the formulary
        """
        channel_layer = get_channel_layer()

        for user in UserExtended.objects.filter(company_id=company_id):
            group_name = 'user_{}'.format(user.id)
            async_to_sync(channel_layer.group_send)(
                '{}'.format(group_name),
                {
                    'type': 'send_formulary_added_or_updated',
                    'data': {
                        'dynamic_form_id': dynamic_form_id,
                        'form_id': form_id,
                        'user_id': updated_user_id,
                        'company_id': company_id
                    }
                }
            )