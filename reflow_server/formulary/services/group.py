from reflow_server.formulary.models import Group
from reflow_server.formulary.services.utils import Settings


class GroupService(Settings):
    def __init__(self, user_id, company_id):
        self.user_id = user_id
        self.company_id = company_id
    
    def save_group(self, instance, name, enabled, order):
        existing_groups = Group.objects.filter(company_id=self.context['company_id']).exclude(id=self.instance.id if self.instance else None)

        self.update_order(existing_groups, order)
        is_new = instance.id == None

        instance.company_id = self.company_id
        instance.enabled = enabled
        instance.name = name
        instance.order = order
        instance.save()

        return instance