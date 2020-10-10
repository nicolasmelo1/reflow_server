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
            django.db.models.QuerySet(reflow_server.theme.models.ThemeKanbanCard): A queryset of the ThemeKanbanCard instances of this theme.
        """
        return self.get_queryset().filter(theme_id=theme_id)

    def create_theme_kanban_card(self, theme_instance, is_default=False):
        """
        Creates a new ThemeKanbanCard instance in the database.

        Args:
            theme_instance (reflow_server.theme.models.Theme): For which theme does this ThemeKanbanCard is bound to.
            is_default (bool, optional): is it default or not. With this when the user opens the 
                                         kanban for the first time after selecting a theme, the kanban
                                         card appears already selected. Defaults to False.

        Returns:
            reflow_server.theme.models.ThemeKanbanCard: The created ThemeKanbanCard instance
        """
        return self.get_queryset().create(
            default=is_default,
            theme=theme_instance
        )