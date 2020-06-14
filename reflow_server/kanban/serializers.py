from django.db import transaction

from rest_framework import serializers

from reflow_server.kanban.models import KanbanCard, KanbanCardField, KanbanDimensionOrder
from reflow_server.kanban.services import KanbanService
from reflow_server.kanban.relations import GetKanbanFieldsRelation, KanbanCardFieldRelation
from reflow_server.data.models import DynamicForm, FormValue
from reflow_server.data.services.formulary import FormularyDataService


class GetKanbanSerializer(serializers.Serializer):
    default_kanban_card_id = serializers.IntegerField()
    default_dimension_field_id = serializers.IntegerField()
    dimension_fields = GetKanbanFieldsRelation(many=True)
    fields = GetKanbanFieldsRelation(many=True)

    def __init__(self, user_id, company_id, form_name, *args, **kwargs):
        """
        This serializer is responsible for loading the initial and required data to load the kanban,
        kanban visualization has some data saved and that needs to be retrieved by the client in order to load
        the visualization.

        Args:
            user_id (int): The id of the user for who you are requesting this kanban render to
            company_id (int): Okay, we got the id, but for which company.
            form_name (str): Kanban visualization is always bound to a formulary, you could not have a kanban visualization
            for multiple forms at the same time.
        """
        self.kanban_service = KanbanService(user_id, company_id, form_name)

        kwargs['data'] = {
            'default_kanban_card_id': self.get_default_kanban_card_id,
            'default_dimension_field_id': self.get_default_dimension_field_id,
            'dimension_fields': self.get_dimension_fields,
            'fields': self.get_filter_fields
        }
        super(GetKanbanSerializer, self).__init__(**kwargs)
        self.is_valid()
    
    @property
    def get_default_kanban_card_id(self):
        return self.kanban_service.get_default_kanban_card_id
    
    @property
    def get_default_dimension_field_id(self):
        return self.kanban_service.get_default_dimension_field_id

    @property
    def get_filter_fields(self):
        return GetKanbanFieldsRelation(instance=self.kanban_service.get_fields, many=True).data
    
    @property
    def get_dimension_fields(self):
        return GetKanbanFieldsRelation(instance=self.kanban_service.get_possible_dimension_fields, many=True).data


class KanbanCardsSerializer(serializers.ModelSerializer):
    """
    This view handles kanban_cards data, you should note that these kanban cards are the cards to build the kanban, 
    not the actual data that is displayed to the user.
    """
    id = serializers.IntegerField(allow_null=True, required=False)
    kanban_card_fields = KanbanCardFieldRelation(many=True)

    def save(self, user_id, **kwargs):
        self.user_id = user_id
        return super(KanbanCardsSerializer, self).save(**kwargs)

    @transaction.atomic
    def create(self, validated_data):
        instance = KanbanCard.objects.create(user_id=self.user_id)
        # save kanban card fields
        for field in validated_data.get('kanban_card_fields'):
            KanbanCardField.objects.create(kanban_card=instance, field_id=field['field']['id'])
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        # deletes all of the kanban fields
        KanbanCardField.objects.filter(kanban_card=instance).delete()
        # save kanban card fields
        for field in validated_data.get('kanban_card_fields'):
            KanbanCardField.objects.create(kanban_card=instance, field_id=field['field']['id'])
        return instance

    class Meta:
        model = KanbanCard
        fields = ('id', 'kanban_card_fields')


class KanbanDefaultsSerializer(serializers.Serializer):
    """
    This serializer is responsible for saving the default kanban_card_id to be retrieved when the user
    opens the kanban again. So when the user opens the kanban in a particular company and for a particular
    form, the kanban is `automagically` loaded for him.
    """
    default_kanban_card_id = serializers.IntegerField()

    def save(self, user_id, company_id, form_name):
        kanban_service = KanbanService(user_id=user_id, company_id=company_id, form_name=form_name)
        kanban_service.save_defaults(self.validated_data['default_kanban_card_id'])


class KanbanDimensionOrderListSerializer(serializers.ListSerializer):
    @transaction.atomic
    def update(self, instance, validated_data):
        for index, element in enumerate(instance):
            element.options = validated_data[index]['options']
            element.order = index
            element.save()
        return instance


class KanbanDimensionOrderSerializer(serializers.ModelSerializer):
    """
    This serializer is used to display dimensionOrders and also updating the order of each KanbanDimensionOrder
    """
    options = serializers.CharField()

    class Meta:
        model = KanbanDimensionOrder
        list_serializer_class = KanbanDimensionOrderListSerializer
        fields = ('options',)


class ChangeKanbanCardBetweenDimensionsSerializer(serializers.Serializer):
    """
    Serializer used for when changing a dimension of a card
    """
    new_value = serializers.CharField()
    form_value_id = serializers.IntegerField()

    def __init__(self,user_id, company_id, form_name, **kwargs):
        self.formulary_data_service = FormularyDataService(user_id=user_id, company_id=company_id, form_name=form_name)
        super(ChangeKanbanCardBetweenDimensionsSerializer, self).__init__(**kwargs)
    
    def validate(self, data):
        form_value_to_change = FormValue.objects.filter(id=data['form_value_id']).first()
        sections = DynamicForm.objects.filter(depends_on_id=form_value_to_change.form.depends_on.id)
        
        formulary_data = self.formulary_data_service.add_formulary_data(form_value_to_change.form.depends_on.id)
        for section in sections:
            section_data = formulary_data.add_section_data(section_id=section.form.id, section_data_id=section.id)
            section_field_values = FormValue.objects.filter(form_id=section.id)
            for field_value in section_field_values:
                value = data['new_value'] if field_value.id == form_value_to_change.id else field_value.value
                section_data.add_field_value(field_value.field.name, value, field_value.id)
        if self.formulary_data_service.is_valid():
            return data
        else:
            raise serializers.ValidationError(detail=self.formulary_data_service.errors)
        

    def save(self):
        instance = self.formulary_data_service.save()
        return instance