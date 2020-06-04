from django.db import transaction

from reflow_server.formulary.models import Field, FormValue, OptionAccessedBy
from reflow_server.kanban.models import KanbanCard, KanbanCardField, KanbanDimensionOrder
from reflow_server.formulary.services.data import DataService

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
    def get_create_or_update_kanban_dimension_order(self, field_id):
        """
        This function is a helper responsible for creating or updating kanban dimension orders.
        We always call this function when:

        1. you are trying to get each column of the selected kanban dimension
        2. you are selecting a new dimension

        We need this because the options might change when the user opens the formulary, so the kanban needs to change with it.
        
        This function automatically adds a new column if a option is added in the selected dimension and also sets the dimension
        as default in the CURRENT FORMULARY if it is selected (it means a user can have more than 1 default dimension, but it is just ONE default
        dimension PER formulary).

        Arguments:
            field {[reflow_server.formulary.models.Field]} -- the dimension field object (dimension is just a field of `option` type)        
        Returns:
            [Queryset(reflow_server.kanban.models.KanbanDimensionOrder)] -- A queryset with all of the options in the current 
            selected dimension
        """
        dimension = Field.objects.filter(form__depends_on__group__company_id=self.company_id, id=field_id, form__depends_on__form_name=self.form_name).first()
        
        if dimension.type.type in ['option']:
            possible_values = OptionAccessedBy.objects.filter(
                user_id=self.user_id,
                field_option__field=dimension
            ).values_list('field_option__option', flat=True)
        else:
            data_service = DataService(self.user.id, self.company.id)
            form_data_ids = data_service.get_user_form_data_ids_from_form_id(dimension.form.depends_on.id)
            options = FormValue.objects.filter(
                form__depends_on__in=form_data_ids, 
                field=dimension
            ).values_list('value', flat=True).distinct()

            options = [int(option) for option in options]

            possible_values = FormValue.objects.filter(
                form__in=options, 
                field=dimension.form_field_as_option
            ).values_list('value', flat=True).distinct()

        dimension_orders = KanbanDimensionOrder.objects.filter(
            user_id=self.user_id,
            dimension__form__depends_on__form_name=form_name
        )
        dimension_orders.update(default=False)
        dimension_order_values = dimension_orders.filter(dimension=dimension).values_list('options', flat=True)
        if sorted(dimension_order_values) != sorted(possible_values):
            if dimension_order_values.count() > len(possible_values):
                difference_values = [x for x in dimension_order_values if x not in possible_values]
            elif dimension_order_values.count() < len(possible_values):
                difference_values = [x for x in possible_values if x not in dimension_order_values]
            else:
                old_values = [x for x in dimension_order_values if x not in possible_values]
                new_values = [x for x in possible_values if x not in dimension_order_values]
                difference_values = old_values + new_values

            for index, value in enumerate(difference_values):
                if value in dimension_order_values:
                    dimension_order = dimension_orders.filter(options=value)
                    dimension_order.delete()
                else:
                    KanbanDimensionOrder.objects.create(
                        options=value,
                        dimension=dimension, 
                        user_id=self.user_id,
                        order=index
                    )
        dimension_orders = dimension_orders.filter(
            user_id=self.user_id, 
            dimension_id=dimension.id
        ).order_by('order')
        dimension_orders.update(default=True)
        return dimension_orders.order_by('order')

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