from django.conf.urls import re_path, include
from django.conf import settings

from reflow_server.core.decorators import permission_required
from reflow_server.kanban.views import GetKanbanView, KanbanCardsView, KanbanCardsEditView, KanbanSetDefaultsView, \
    KanbanDimensionOrderView, ChangeKanbanCardBetweenDimensionsView

settings_urlpatterns = [
    re_path(r'^card/$', permission_required(KanbanCardsView.as_view()), name='kanban_kanban_cards'),
    re_path(r'^card/(?P<kanban_card_id>\d+)/$', permission_required(KanbanCardsEditView.as_view()), name='kanban_edit_kanban_cards'),
    re_path(r'^defaults/$', permission_required(KanbanSetDefaultsView.as_view()), name='kanban_set_defaults'),
]

urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^$', permission_required(GetKanbanView.as_view()), name='kanban_get_kanban'),
        re_path(r'^change/$', permission_required(ChangeKanbanCardBetweenDimensionsView.as_view()), name='kanban_change_card_between_dimensions'),
        re_path(r'^dimension/(?P<field_id>\w+)/$', permission_required(KanbanDimensionOrderView.as_view()), name='kanban_dimension_order'),
        re_path(r'^settings/', include(settings_urlpatterns))
    ])),
]