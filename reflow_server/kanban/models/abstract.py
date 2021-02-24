from django.db import models


class AbstractKanbanCard(models.Model):
    """
    This abstract holds the kanban Card Data. The Kanban Card itself is really simple. It is just an id to be used for the
    KanbanCardField and if this card is default or not (default means that we'll load that Card first if the user opens
    the kanban visualization, otherwise he have to fill a simple obligatory data form to build the kanban)

    It's worth mentioning that default is default for the formulary and dimension means a `reflow_server.formulary.models.Field`
    with `option` field_type. Each option will be a column for the kanban.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'kanban'


class AbstractKanbanCardField(models.Model):
    """
    If the kanban card holds only the dimension, here we hold the fields of the kanban card. For this we use this
    special model.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        abstract = True
        app_label = 'kanban'
        ordering = ('order',)


class AbstractKanbanDimensionOrder(models.Model):
    """
    This is simple, for you to build a kanban you need to have a:

    1 - Kanban Card - imagine it as being each post it in a kanban-whiteboard (reference: https://netproject.com.br/blog/wp-content/uploads/2016/12/quadro-kanban.jpg)
    2 - The dimension - Is a `reflow_server.formulary.models.Field` with `option` field_type

    Each option will be a column in the Kanban Board. But sometimes you need to reorder the dimension. 
    Sometimes the `Todo` might be the last column, and `Done` must be the first. 

    This model here holds the order of each option. So with this the user can easily reorder what comes 
    first and what comes last.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    options = models.CharField(max_length=500)
    order = models.BigIntegerField()
    default = models.BooleanField(default=False)

    class Meta:
        abstract = True
        app_label = 'kanban'