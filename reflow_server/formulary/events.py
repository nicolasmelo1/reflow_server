from reflow_server.core.utils.channel_layers import ChannelLayer
from reflow_server.authentication.models import UserExtended
from reflow_server.formulary.models import Form


class FormularyBroadcastEvent:
    """
    This class is used for sending real time events about Formularies
    """
    def send_updated_formulary(self, company_id, form_id, section_id=None, field_id=None, is_new_formulary=False, is_new_field=False):
        """
        This event sends to all of the clients of a company that a formulary have been updated

        Args:
            company_id (int): What company updated the formulary
            form_id (int): the id of the formulary/page updated
            is_new_formulary (bool): Is it a new formulary
            is_new_field (bool): Is it a new field
            section_id (int): If a field was updated the section of the field that was updated
            field_id (int): If a field was updated or created, the field_id.
        """
        form_name = Form.formulary_.form_name_by_form_id_and_company_id(form_id, company_id)

        for user in UserExtended.data_.users_active_by_company_id(company_id):
            group_name = 'user_{}'.format(user.id)
            ChannelLayer.broadcast_to_group(group_name, 'send_formulary_created_or_updated', {
                'form_name': form_name,
                'form_id': form_id,
                'company_id': company_id,
                'is_new_formulary': is_new_formulary,
                'is_new_field': is_new_field,
                'section_id': section_id,
                'field_id': field_id
            })
        
    def formulary_created(self, user_id, company_id, form_id):
        self.send_updated_formulary(company_id, form_id, is_new_formulary=True)

    def formulary_updated(self, user_id, company_id, form_id):
        self.send_updated_formulary(company_id, form_id)

    def field_created(self, user_id, company_id, form_id, section_id, field_id):
        self.send_updated_formulary(company_id, form_id, section_id, field_id, is_new_field=True)
    
    def field_updated(self, user_id, company_id, form_id, section_id, field_id):
        self.send_updated_formulary(company_id, form_id, section_id, field_id)
