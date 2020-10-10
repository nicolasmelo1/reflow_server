from django.db import models


class KanbanCardThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def kanban_cards_by_kanban_card_ids(self, kanban_card_ids):
        """
        Retrive a queryset of KanbanCard instances that are in a list of kanban_card_ids

        Args:
            kanban_card_ids (list(int)): A list of KanbanCard instance ids.

        Returns:
            django.db.models.QuerySet(reflow_server.kanban.models.KanbanCard): A queryset of KanbanCards that have 
                                                                        the instance id in the list provided.
        """
        return self.get_queryset().filter(id__in=kanban_card_ids)

    def update_kanban_card_default(self, kanban_card_id, default):
        """
        Updates a single KanbanCard instance `default` attribute.

        Args:
            kanban_card_id (int): The KanbanCard instance id you want to update
            default (bool): Is it default or not, it means when the user opens the formulary, will he open with this KanbanCard
                            already selected or not.

        Returns:
            int: number of instances updated, in this case just 1
        """
        return self.get_queryset().filter(id=kanban_card_id).update(default=default)