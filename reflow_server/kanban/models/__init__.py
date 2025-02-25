from django.db import models

from reflow_server.kanban.models.abstract import AbstractKanbanDimensionOrder, AbstractKanbanCardField, AbstractKanbanCard
from reflow_server.theme.managers import KanbanDimensionThemeManager, KanbanCardThemeManager, \
    KanbanCardFieldThemeManager
    

class KanbanDefault(models.Model):
    """
    Sets the default data of the kanban. This sets the default dimension to be used and also the default kanban card to be used.
    With this, when the user opens the kanban on a particular formulary we automatically build the kanban for him
    """
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    kanban_card = models.ForeignKey('kanban.KanbanCard', models.CASCADE, blank=True, null=True, db_index=True)
    kanban_dimension = models.ForeignKey('formulary.Field', models.CASCADE, blank=True, null=True, db_index=True)

    class Meta:
        db_table = 'kanban_default'

    objects = models.Manager()
    theme_ = KanbanDimensionThemeManager()


class KanbanCollapsedOption(models.Model):
    """
    Collapsed option means that the kanban dimension phase is collapsed, in other words, it's contents are not shown to the user.
    """
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True)
    field_option = models.ForeignKey('formulary.FieldOptions', models.CASCADE, db_index=True)    

    class Meta:
        db_table = 'kanban_collapsed_option'

        
class KanbanCard(AbstractKanbanCard):
    """
    For further explanation refer to `reflow_server.kanban.models.abstract.AbstractKanbanCard`

    It's important to notice that each kanban card is defined on the user level, so each user can have his own
    kanban card for each dimension.
    """
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True)
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True, null=True, default=None)
    form = models.ForeignKey('formulary.Form', models.CASCADE, db_index=True, null=True, default=None)

    class Meta:
        db_table = 'kanban_card'
        app_label = 'kanban'

    objects = models.Manager()
    theme_ = KanbanCardThemeManager()


class KanbanCardField(AbstractKanbanCardField):
    """
    For further explanation refer to `reflow_server.kanban.models.abstract.AbstractKanbanCardField`

    This just holds the fields that must be displayed when the user select a kanban card. These are the fields that
    are loaded on the front end.
    """
    field = models.ForeignKey('formulary.Field', models.CASCADE, blank=True, null=True)
    kanban_card = models.ForeignKey('kanban.KanbanCard', models.CASCADE, blank=True, null=True,
                                    related_name='kanban_card_fields',  db_index=True)

    class Meta:
        db_table = 'kanban_card_field'
        app_label = 'kanban'
        ordering = ('order',)
        
    objects = models.Manager()
    theme_ = KanbanCardFieldThemeManager()


class KanbanDimensionOrder(AbstractKanbanDimensionOrder):
    """
    TODO: DEPRECATED
    For further explanation refer to `reflow_server.kanban.models.abstract.AbstractKanbanDimensionOrder`

    Also the same as kanban card, we define the order for each dimension on the user level, not company level
    If the user wants define a different order for the kanban than the rest of the company is using, he can.

    We prefer to give more freedom for the user in our plataform, and not to be tightly coupled with the company.
    Each user has it's own way of working we think.
    """
    dimension = models.ForeignKey('formulary.Field', models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE)

    class Meta:
        db_table = 'kanban_dimension_order'
        app_label = 'kanban'

    objects = models.Manager()
