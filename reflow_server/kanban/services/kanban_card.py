from django.db import transaction

from reflow_server.kanban.models import KanbanCard, KanbanCardField


class KanbanCardService:
    def __init__(self, user_id):
        self.user_id = user_id

    @transaction.atomic
    def save_kanban_card(self, instance, field_ids):
        """
        Creates or updates a Kanban Card data, with it's fields.
        For it you need to send the field_ids as list in the parameter, so we can update all of the fields of the kanban card

        Args:
            instance (reflow_server.kanban.models.KanbanCard): The instance of the KanbanCard to update or to create
            field_ids (list(int)): List of field_ids to use on the kanban card

        Returns:
            reflow_server.kaban.models.KanbanCard: The newly created or updated KanbanCard
        """
        
        if instance:
            KanbanCardField.objects.filter(kanban_card=instance).delete()

        instance.user_id = self.user_id
        instance = instance.save()

        for field_id in field_ids:
            KanbanCardField.objects.create(kanban_card=instance, field_id=field_id)
        return instance