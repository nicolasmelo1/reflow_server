from reflow_server.formulary.models import Group
from reflow_server.formulary.services.utils import Settings


class GroupService(Settings):
    def __init__(self, company_id):
        self.company_id = company_id
    
    def update_group(self, instance, name, enabled, order):
        """
        Updates a Group instance with new data. Usually groups are just a group of formularies.

        Args:
            instance (reflow_server.formulary.models.Group): The group instance to update, you don't need to send the id
            here you pass the hole instance to update.
            name (str): This name is the name of the group, you can name everything you want.
            enabled (bool): Wheather the Group is enabled or not. Enabled means that it won't show to the users (except admins) 
            but it's data and content will be preserved.
            order (int): The ordering of this group, ordering is how it should be ordered in the screen for the user.

        Returns:
            reflow_server.formulary.models.Group: The Group instance updated. If it is not an instance it will return
            the value you sent on the instance attribute.
        """
        if instance:
            existing_groups = Group.objects.filter(company_id=self.company_id).exclude(id=instance.id if instance else None)

            self.update_order(existing_groups, order)

            instance.company_id = self.company_id
            instance.enabled = enabled
            instance.name = name
            instance.order = order
            instance.save()

        return instance

    def create_group(self, name):
        """
        Creates a new Group instance in the database.

        Args:
            name (str):  This name is the name of the group, you can name everything you want. Usually we only create groups based
            on themes. So this will get the template group name. So if you selected the template `customer success control` from `sales` 
            this group will have the `sales` name.

        Returns:
            reflow_server.formulary.models.Group: The newly created Group instance.
        """
        existing_groups = Group.objects.filter(company_id=self.company_id).order_by('-order')
        if existing_groups:
            order = existing_groups[0].order + 1
        else:
            order = 1
        
        self.update_order(existing_groups, order)

        instance = Group.objects.create(
            company_id=self.company_id,
            enabled=True,
            order=order,
            name=name
        )

        return instance
