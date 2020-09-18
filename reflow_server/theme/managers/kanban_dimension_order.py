from django.db import models


class KanbanDimensionOrderThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def create_kanban_dimension_order(self, dimension_id, order, default, user_id, option):
        """
        Creates a new kanban dimension order. We don't use services here because you will notice that
        on KanbanService that kanban dimension orders are automatically generated, here we need to 
        follow the default order estipulated in the theme.

        Args:
            dimension_id (int): This is just a reflow_server.formulary.models.Field instance id that represents
            the dimension that should be used.
            order (int): The order of this dimension.
            default (bool): Is this dimension default or not, it means when the user first loads the kanban of this formulary
            it should be the default dimension selected or not?
            user_id (int): the id of a instance of type reflow_server.authentication.models.UserExtended
            option (str): We don't bound the kanban to any FieldOption or nothing, we bound to a specific value, so if the option 
            change or something change this is not affected. Also we can create kanban of many field types.

        Returns:
            reflow_server.kanban.models.KanbanDimensionOrder: The newly created KanbanDimensionOrder model instance.
        """
        return self.get_queryset().create(
            dimension_id=dimension_id,
            order=order,
            default=default,
            user_id=user_id,
            options=option
        )