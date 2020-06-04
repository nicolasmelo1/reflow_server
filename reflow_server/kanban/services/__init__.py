from django.db import transaction

from reflow_server.formulary.models import Field
from reflow_server.kanban.models import KanbanCard, KanbanCardField, KanbanDimensionOrder


class KanbanService:
    def __init__(self, user_id, company_id, form_name):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name
    
        self.__fields = Field.objects.filter(
            form__depends_on__group__company_id=company_id,
            form__depends_on__form_name=form_name,
        ).order_by('order')

    @transaction.atomic
    def save_defaults(self, kanban_card_id):
        kanban_cards = self.get_kanban_cards
        kanban_cards.update(default=False)
        kanban_cards.filter(id=kanban_card_id).update(default=True)

    @property
    def get_fields(self):
        return self.__fields
    
    @property
    def get_possible_dimension_fields(self):
        return self.__fields.filter(type__type__in=['form', 'option'])
    
    @property
    def get_kanban_cards(self):
        # get kanban card ids of this form_name and this user
        kanban_card_ids = KanbanCardField.objects.filter(
            field__form__depends_on__form_name=self.form_name, 
            field__form__depends_on__group__company_id=self.company_id,
            kanban_card__user_id=self.user_id
        ).values_list('kanban_card', flat=True).distinct()
        return KanbanCard.objects.filter(id__in=kanban_card_ids)

    @property
    def get_default_kanban_card_id(self):
        return self.get_kanban_cards.filter(default=True).values_list('id', flat=True).first()
    
    @property
    def get_default_dimension_field_id(self):
        return KanbanDimensionOrder.objects.filter(
            user_id=self.user_id,
            default=True,
            dimension__form__depends_on__form_name=self.form_name
        ).values_list('dimension_id', flat=True).distinct().first()