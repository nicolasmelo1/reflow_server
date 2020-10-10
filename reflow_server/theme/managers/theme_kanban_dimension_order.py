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
            django.db.models.QuerySet(reflow_server.theme.models.ThemeKanbanDimensionOrder): Returns
            a queryset of ThemeKanbanDimensionOrder instances ordered.
        """
        return self.get_queryset().filter(theme_id=theme_id).order_by('order')

    def create_theme_kanban_dimension_order(self, theme_instance, dimension_id, option, order, is_default=False):
        """
        Creates a new ThemeKanbanDimensionOrder instance.

        Args:
            theme_instance (reflow_server.theme.models.Theme): For which theme does this ThemeKanbanDimension is bound to.
            dimension_id (int): A ThemeField instance id to be used as dimension
            option (int): The dimension options on the kanban (each column) are not bound to anything, they are simple string
                          this way, even if the options are deleted we can still have the dimension. Also with this the dimension
                          can work on `form` field types
            order (int): The order of the dimension option
            is_default (bool, optional): Is the ThemeKanbanDimensionOrder default or not. This way when the user selects the theme, this
                                         dimension already appears selected for the user. Defaults to False.

        Returns:
            reflow_server.theme.models.ThemeKanbanDimensionOrder: Returns the created ThemeKanbanDimensionOrder instance
        """
        return self.get_queryset().create(
            dimension_id=dimension_id,
            order=order,
            default=is_default,
            theme=theme_instance,
            options=option
        )