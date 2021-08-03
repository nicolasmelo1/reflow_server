from reflow_server.core.utils.channel_layers import ChannelLayer
from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.models import Form


class DataBroadcastEvent:
    """
    This class is used for sending real time events for the client about this service
    """ 
    def send_updated_formulary(self, company_id, dynamic_form_id, form_id, updated_user_id):
        """
        This event sends to all of the clients of a company that a formulary data have been updated or inserted

        Arguments:
            company_id {int} -- What company updated the formulary
            dynamic_form_id {int} -- the id of the formulary data added or updated
            form_id {int} -- the id of the formulary/page updated
            updated_user_id {int} -- what user id updated the formulary
        """
        form_name = Form.data_.form_name_by_form_id_and_company_id(form_id, company_id)
        for user in UserExtended.data_.users_active_by_company_id(company_id):
            group_name = 'user_{}'.format(user.id)
            ChannelLayer.broadcast_to_group(group_name, 'send_formulary_data_added_or_updated', {
                'dynamic_form_id': dynamic_form_id,
                'form_id': form_id,
                'form_name': form_name,
                'user_id': updated_user_id,
                'company_id': company_id
            })

    def formulary_data_updated(self, user_id, company_id, form_id, form_data_id, is_public):
        self.send_updated_formulary(company_id, form_data_id, form_id, user_id)

    def formulary_data_created(self, user_id, company_id, form_id, form_data_id, is_public):
        self.send_updated_formulary(company_id, form_data_id, form_id, user_id)