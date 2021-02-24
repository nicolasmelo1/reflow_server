from django.db import transaction
from django.db.models import Q

from reflow_server.formulary.models import Field, FieldOptions, Form, OptionAccessedBy
from reflow_server.data.models import FormValue
from reflow_server.kanban.services.kanban_card import KanbanCardService
from reflow_server.kanban.models import KanbanCard, KanbanCardField, KanbanDimensionOrder, KanbanDefault
from reflow_server.data.services import DataService

class KanbanValidationError(AttributeError):
    pass

class KanbanService(KanbanCardService):
    def __init__(self, user_id, company_id, form_name=None, form=None):
        self.user_id = user_id
        self.company_id = company_id
        self.form = Form.objects.filter(form_name=form_name, depends_on__isnull=True).first() if form_name != None else form
    
        self.__fields = Field.objects.filter(
            form__depends_on__group__company_id=company_id,
            form__depends_on=self.form,
        ).order_by('order')

    @staticmethod
    def copy_defaults_to_company_user(company_id, from_user_id, to_user_id):
        kanban_defaults = KanbanDefault.objects.filter(
            user_id=from_user_id,
            company_id=company_id
        )
        for kanban_default in kanban_defaults:
            if kanban_default.kanban_card:
                default_kanban_card = KanbanCard.objects.create(
                    form=kanban_default.kanban_card.form,
                    company_id=company_id,
                    user_id=to_user_id
                )
                for kanban_card_fields_to_copy in KanbanCardField.objects.filter(kanban_card=kanban_default.kanban_card):
                    KanbanCardField.objects.create(
                        field=kanban_card_fields_to_copy.field,
                        kanban_card=default_kanban_card,
                        order=kanban_card_fields_to_copy.order
                    )
            else:
                default_kanban_card = kanban_default.kanban_card
            
            KanbanDefault.objects.create(
                form=kanban_default.form,
                company_id=company_id,
                user_id=to_user_id,
                kanban_card=default_kanban_card,
                kanban_dimension=kanban_default.kanban_dimension
            )
    def are_defaults_valid(self, kanban_card_id, kanban_dimension_id):
        """
        Check if the default values you are trying to set are valid before saving.

        Args:
            kanban_card_id ([type]): [description]
            kanban_dimension_id ([type]): [description]

        Returns:
            [type]: [description]
        """
        self._was_defaults_validated = True

        if not self.get_kanban_cards.filter(id=kanban_card_id).exists() or kanban_card_id == None:
            return False
        if not self.get_possible_dimension_fields.filter(id=kanban_dimension_id).exists() or kanban_dimension_id == None:
            return False
        return True

    @transaction.atomic
    def save_defaults(self, kanban_card_id, kanban_dimension_id):
        """
        This saves the default configurations so when the user opens the kanban again on a certain formulary 
        the data is loaded automatically for him.

        Args:
            kanban_card_id (int):
            kanban_dimension_id (int):
        """
        if not hasattr(self, '_was_defaults_validated'):
            raise KanbanValidationError('You need to validate the defaults using `.are_defaults_valid()` method before saving.')
        instance = KanbanDefault.objects.update_or_create(
            form=self.form,
            user_id=self.user_id,
            company_id=self.company_id,
            defaults={
                'kanban_card_id': kanban_card_id,
                'kanban_dimension_id': kanban_dimension_id
            }
        )

        return instance


    @property
    def get_fields(self):
        return self.__fields
    
    @property
    def get_possible_dimension_fields(self):
        return self.__fields.filter(type__type='option')

    def get_dimension_phases(self, dimension_id):
        field_option_ids = OptionAccessedBy.kanban_.field_options_by_user_id_and_field_id(self.user_id, dimension_id)
        return FieldOptions.kanban_.field_options_by_field_option_ids_and_company_id(field_option_ids, self.company_id)

    @property
    def get_kanban_cards(self):
        # get kanban card ids of this form_name and this user
        kanban_card_ids = KanbanCardField.objects.filter(
            field__form__depends_on=self.form, 
            field__form__depends_on__group__company_id=self.company_id,
            kanban_card__user_id=self.user_id
        ).values_list('kanban_card', flat=True).distinct()
        return KanbanCard.objects.filter(id__in=kanban_card_ids)

    