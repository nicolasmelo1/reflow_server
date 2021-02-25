from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.authentication.services.routes import register_admin_only_url
from reflow_server.kanban.views import KanbanFieldsView, KanbanCardsView, KanbanCardsEditView, KanbanDefaultView, \
    KanbanEditDefaultView, KanbanDimensionPhaseView, ChangeKanbanCardBetweenDimensionsView, KanbanChangeDimensionPhasesView

settings_urlpatterns = [
    re_path(r'^card/$', validate_billing(KanbanCardsView.as_view()), name='kanban_kanban_cards'),
    re_path(r'^card/(?P<kanban_card_id>\d+)/$', validate_billing(KanbanCardsEditView.as_view()), name='kanban_edit_kanban_cards'),
    re_path(r'^fields/$', validate_billing(KanbanFieldsView.as_view()), name='kanban_fields'),
    re_path(r'^default/$', validate_billing(KanbanEditDefaultView.as_view()), name='kanban_edit_default'),
    register_admin_only_url(
        re_path(r'^dimension/(?P<field_id>\w+)/$', validate_billing(KanbanChangeDimensionPhasesView.as_view()), name='kanban_change_dimension_phases')
    )
]

urlpatterns = [
    re_path(r'(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<form>\w+)/', include([
        re_path(r'^default/$', validate_billing(KanbanDefaultView.as_view()), name='kanban_default'),
        re_path(r'^change/$', validate_billing(ChangeKanbanCardBetweenDimensionsView.as_view()), name='kanban_change_card_between_dimensions'),
        re_path(r'^dimension/(?P<field_id>\w+)/$', validate_billing(KanbanDimensionPhaseView.as_view()), name='kanban_dimension_order'),
        re_path(r'^settings/', include(settings_urlpatterns))
    ])),
]