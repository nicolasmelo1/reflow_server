from reflow_server.authentication.models import UserExtended
from reflow_server.draft.services import DraftService
from reflow_server.core.utils.channel_layers import ChannelLayer


class DraftBroadcastEvent:
    """
    This class is used for sending real time events for the client about this domain
    """
    def remove_old_draft(self, user_id, company_id, draft_id, draft_is_public):
        """
        This event sends to all of the clients of the company that
        a draft has been removed from the backend.

        Args:
            user_id (int): The UserExtended instance id.
            company_id (int): What company was the formulary
            draft_id (int): The draft id used to be transformed into a draft_string_id
            draft_is_public (bool): If the draft is public then send to the public consumer,
                                    otherwise sends to the user consumers.
        """
        draft_string_id = DraftService.draft_id_to_draft_string_id(draft_id)
        if draft_is_public:
            ChannelLayer.broadcast_to_group('public', 'send_public_removed_draft', {
                'draft_string_id': draft_string_id
            })
        else:
            user_ids = UserExtended.draft_.user_ids_active_by_company_id(company_id)

            for user_id in user_ids:
                group_name = 'user_{}'.format(user_id)
                ChannelLayer.broadcast_to_group(group_name, 'send_removed_draft', {
                    'company_id': company_id,
                    'draft_string_id': draft_string_id
                })