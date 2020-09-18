from django.db import models


class ThemeKanbanDimensionOrderThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_kanban_dimension_order_by_theme_id_ordered(self, theme_id):
        """
        Retrieves a queryset of ordered ThemeKanbanDimensionOrder instances from the theme_id.

        Args:
            theme_id (int): The id of a single Theme instance.

        Returns:
            django.db.QuerySet(reflow_server.theme.models.ThemeKanbanDimensionOrder): Returns
            a queryset of ThemeKanbanDimensionOrder instances ordered.
        """
        return self.get_queryset().filter(theme_id=theme_id).order_by('order')