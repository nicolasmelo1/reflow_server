from rest_framework import status

from reflow_server.kanban.models import KanbanCard
from reflow_server.core.permissions import PermissionsError


class KanbanDefaultPermission:
    """
    Read reflow_server.core.permissions for further reference on what's this and how it works. So you can create 
    your own custom permission classes.
    """
    def __init__(self, kanban_card_id=None):
        self.kanban_card_id = kanban_card_id

    def __call__(self, request):
        if self.kanban_card_id and not KanbanCard.objects.filter(id=self.kanban_card_id, user=request.request.user.id).exists():
            raise PermissionsError(detail='not_permitted', status=status.HTTP_404_NOT_FOUND)
