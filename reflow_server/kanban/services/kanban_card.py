from django.db import transaction

from reflow_server.kanban.models import KanbanCard, KanbanCardField


class KanbanCardService:
    def __init__(self, user_id):
        self.user_id = user_id

    @transaction.atomic
    def save_kanban_card(self, field_ids, instance=None):
        """
        Creates or updates a Kanban Card data, with it's fields.
        For it you need to send the field_ids as list in the parameter, so we can update all of the fields of the kanban card

        Args:
            field_ids (list(int)): List of field_ids to use on the kanban card
            instance (reflow_server.kanban.models.KanbanCard, optional): The instance of the KanbanCard to update or to create.
            Defaults to reflow_server.kanban.models.KanbanCard.

        Returns:
            reflow_server.kaban.models.KanbanCard: The newly created or updated KanbanCard
        """
        if instance:
            KanbanCardField.objects.filter(kanban_card=instance).delete()
        else:
            instance = KanbanCard()
            
        instance, __ = KanbanCard.objects.update_or_create(
            id=instance.id if instance else None,
            defaults={
                'user_id': self.user_id
            }
        )

        for index, field_id in enumerate(field_ids):
            KanbanCardField.objects.create(kanban_card=instance, field_id=field_id, order=index)
        return instance