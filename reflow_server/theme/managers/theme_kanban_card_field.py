from django.db import models


class ThemeKanbanCardFieldThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_field_ids_by_theme_kanban_card_id(self, theme_kanban_card_id):
        """
        Returns a queryset of ThemeKanbanCardField instances from a specific theme_kanban_card_id

        Args:
            theme_kanban_card_id (int): A id of a reflow_server.theme.models.ThemeKanbanCard instance

        Returns:
            django.db.models.QuerySet(reflow_server.theme.models.ThemeKanbanCardField): Returns a queryset of
            ThemeKanbanCardField instances from a specific theme_kanban_card_id.
        """
        return self.get_queryset().filter(kanban_card_id=theme_kanban_card_id).values_list('field_id', flat=True)
    
    def create_theme_kanban_card_field(self, theme_kanban_card_id, theme_field_id):
        return self.get_queryset().create(
            kanban_card_id=theme_kanban_card_id,
            field_id=theme_field_id
        )