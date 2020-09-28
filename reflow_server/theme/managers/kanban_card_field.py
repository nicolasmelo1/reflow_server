from django.db import models


class KanbanCardFieldThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def kanban_card_fields_by_kanban_card_id_ordered_by_id(self, kanban_card_id):
        """
        Returns a queryset of KanbanCardField instances ordered by id and that are bound to a single KanbanCardId.
        We order by id since KanbanCardField does not have an ordering, the ordering is the id.

        Args:
            kanban_card_id (int): A kanbanCard instance id to filter the KanbanCardFields

        Returns:
            django.db.QuerySet(reflow_server.kanban.models.KanbanCardField): A queryset of KanbanCardField ordered by id
                                                                             and filtered by the kanban_card_id.
        """
        return self.get_queryset().filter(kanban_card_id=kanban_card_id).order_by('id')

    def kanban_card_ids_by_user_id_company_id_and_main_form_ids(self, user_id, company_id, main_form_ids):
        """
        Returns a queryset of KanbanCard instance ids of a single user_id, a single company and specially
        from a list of main_form_ids. This list holds the ids of the Form instances those fields are bound to.

        Args:
            user_id (int): A UserExtended instance to filter the kanban_card_ids from, usually the user that has created the kanban card
            company_id (int): A Company instance id to filter the kanban_cards from, this way we guarantee we are only filtering the data
                              of a specific company.
            main_form_ids (list(int)): A list of Form instance ids, those are from MAIN FORMS (so instances with depends_on = None)

        Returns:
            django.db.QuerySet(int): A Queryset of ints, the ints here are KanbanCard instance ids.
        """
        return self.get_queryset().filter(
            kanban_card__user_id=user_id, 
            field__form__depends_on__in=main_form_ids, 
            field__form__depends_on__group__company_id=company_id
        ).values_list('kanban_card_id', flat=True)