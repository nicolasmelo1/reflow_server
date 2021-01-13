from channels.layers import get_channel_layer

from asgiref.sync import async_to_sync

from reflow_server.authentication.models import UserExtended


class DraftEvents:
    """
    This class is used for sending real time events for the client about this domain
    """
    def send_removed_draft(self, company_id, draft_string_id):
        """
        This event sends to all of the clients of the company that
        a draft has been removed from the backend.

        Arguments:
            company_id {int} -- What company was the formulary
        """
        channel_layer = get_channel_layer()

        self.cached_users = getattr(self, 'cached_users', {})
        if company_id not in self.cached_users:
            self.cached_users[company_id] = UserExtended.draft_.users_active_by_company_id(company_id)

        for user in self.cached_users[company_id]:
            group_name = 'user_{}'.format(user.id)
            async_to_sync(channel_layer.group_send)(
                '{}'.format(group_name),
                {
                    'type': 'send_removed_draft',
                    'data': {
                        'company_id': company_id,
                        'draft_string_id': draft_string_id
                    }
                }
            )