from django.db import models
from reflow_server.visualization.models.abstract import AbstractKanbanCard, AbstractKanbanCardField, \
    AbstractKanbanDimensionOrder, AbstractListingTotalForField


class VisualizationType(models.Model):
    name = models.CharField(max_length=250)
    label_name = models.CharField(max_length=200)

    class Meta:
        db_table = 'data_type'


class KanbanCard(AbstractKanbanCard):
    """
    For further explanation refer to `reflow_server.visualization.models.abstract.AbstractKanbanCard`

    It's important to notice that each kanban card is defined on the user level, so each user can have his own
    kanban card for each dimension.
    """
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'kanban_card'
        app_label = 'visualization'


class KanbanCardField(AbstractKanbanCardField):
    """
    For further explanation refer to `reflow_server.visualization.models.abstract.AbstractKanbanCardField`

    This just holds the fields that must be displayed when the user select a kanban card. These are the fields that
    are loaded on the front end.
    """
    field = models.ForeignKey('formulary.Field', models.CASCADE, blank=True, null=True)
    kanban_card = models.ForeignKey('visualization.KanbanCard', models.CASCADE, blank=True, null=True,
                                    related_name='kanban_card_fields',  db_index=True)

    class Meta:
        db_table = 'kanban_card_field'
        app_label = 'visualization'


class KanbanDimensionOrder(AbstractKanbanDimensionOrder):
    """
    For further explanation refer to `reflow_server.visualization.models.abstract.AbstractKanbanDimensionOrder`

    Also the same as kanban card, we define the order for each dimension on the user level, not company level
    If the user wants define a different order for the kanban than the rest of the company is using, he can.

    We prefer to give more freedom for the user in our plataform, and not to be tightly coupled with the company.
    Each user has it's own way of working we think.
    """
    dimension = models.ForeignKey('formulary.Field', models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE)

    class Meta:
        db_table = 'kanban_dimension_order'
        app_label = 'visualization'



class ListingSelectedFields(models.Model):
    """
    This is kinda dumb, but it just holds which of the fields needs to be visible in the listing table.
    If the user unselects a field, the column of the table is hidden for the user. If it is displayed, 
    the column is displayed. 
    
    Unlike kanban card fields this doesn't filter the data, that is loaded on the front end. Because on Kanban
    when the user selects another Kanban Card all of the columns go back to page 1. On listing when the user selects
    a new field to display on the column, the pagination doesn't change. 
    """
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)

    class Meta:
        db_table = 'listing_selected_fields'
        app_label = 'visualization'


class ListingTotalForField(AbstractListingTotalForField):
    # TODO: move this to dashboard. this is deprecated.
    # might be deleted later , it will be defined on Dashboard tables
    field = models.ForeignKey('formulary.Field', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    number_configuration_number_format_type = models.ForeignKey('formulary.FieldNumberFormatType', on_delete=models.CASCADE, db_index=True, default=1)

    class Meta:
        db_table = 'listing_total_for_fields'
        app_label = 'visualization'