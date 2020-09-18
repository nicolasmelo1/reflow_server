from django.db import models


class ThemeKanbanCardThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_kanban_cards_by_theme_id(self, theme_id):
        """
        Retrieves a queryset of ThemeKanbanCards based on a theme_id

        Args:
            theme_id (int): This is reflow_server.theme.models.Theme instance id

        Returns:
            django.db.QuerySet(reflow_server.theme.models.Theme): A queryset of the ThemeKanbanCard instances of this theme.
        """
        return self.get_queryset().filter(theme_id=theme_id)