from reflow_server.kanban.managers import field_options
from django.db import transaction

from rest_framework import serializers

from reflow_server.formulary.models import FieldOptions, Field
from reflow_server.formulary.services.fields import FieldService
from reflow_server.formulary.services.data import FieldOptionsData


from reflow_server.kanban.models import KanbanCard, KanbanDefault, KanbanCollapsedOption
from reflow_server.kanban.services import KanbanService
from reflow_server.kanban.relations import KanbanFieldsRelation, KanbanCardFieldRelation
from reflow_server.data.models import DynamicForm, FormValue
from reflow_server.data.services.formulary import FormularyDataService
from reflow_server.data.services.representation import RepresentationService


class KanbanFieldsSerializer(serializers.Serializer):
    dimension_fields = KanbanFieldsRelation(many=True)
    fields = KanbanFieldsRelation(many=True)

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
        self.kanban_service = KanbanService(user_id, company_id, form_name=form_name)

        kwargs['data'] = {
            'dimension_fields': self.get_dimension_fields,
            'fields': self.get_filter_fields
        }
        super(KanbanFieldsSerializer, self).__init__(**kwargs)
        self.is_valid()
    
    @property
    def get_filter_fields(self):
        return KanbanFieldsRelation(instance=self.kanban_service.get_fields, many=True).data
    
    @property
    def get_dimension_fields(self):
        return KanbanFieldsRelation(instance=self.kanban_service.get_possible_dimension_fields, many=True).data


class KanbanCardsSerializer(serializers.ModelSerializer):
    """
    This serializer handles kanban_cards data, you should note that these kanban cards are the cards to build the kanban, 
    not the actual data that is displayed to the user.
    """
    id = serializers.IntegerField(allow_null=True, required=False)
    kanban_card_fields = KanbanCardFieldRelation(many=True)

    def save(self, user_id, company_id, form_name, **kwargs):
        self.kanban_service = KanbanService(user_id, company_id, form_name=form_name)
        return super(KanbanCardsSerializer, self).save(**kwargs)

    def create(self, validated_data):
        field_ids = [field['field']['id'] for field in validated_data.get('kanban_card_fields')]
        instance = self.kanban_service.save_kanban_card(field_ids)
        return instance

    def update(self, instance, validated_data):
        field_ids = [field['field']['id'] for field in validated_data.get('kanban_card_fields')]
        instance = self.kanban_service.save_kanban_card(field_ids, instance)
        return instance

    class Meta:
        model = KanbanCard
        fields = ('id', 'kanban_card_fields')


class KanbanDefaultSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for saving the default kanban_card_id to be retrieved when the user
    opens the kanban again. So when the user opens the kanban in a particular company and for a particular
    form, the kanban is `automagically` loaded for him.
    """
    kanban_card = KanbanCardsSerializer()
    kanban_dimension = KanbanFieldsRelation()

    def validate(self, data):
        self.kanban_service = KanbanService(user_id=self.context['user_id'], company_id=self.context['company_id'], form_name=self.context['form_name'])
        self.kanban_service.are_defaults_valid(data['kanban_card']['id'], data['kanban_dimension']['id'])

        return data

    def save(self):
        self.kanban_service.save_defaults(self.validated_data['kanban_card']['id'], self.validated_data['kanban_dimension']['id'])

    class Meta:
        model = KanbanDefault
        fields = ('kanban_card', 'kanban_dimension')


class KanbanDimensionListSerializer(serializers.ListSerializer):
    @transaction.atomic
    def update(self, instances, validated_data):
        field_instance = Field.objects.filter(id=self.context['field_id']).first()
        field_service = FieldService(
            user_id=self.context['user_id'], 
            company_id=self.context['company_id'], 
            form_id=field_instance.form.depends_on_id
        )
        field_options_data = FieldOptionsData()
        for field_option in validated_data:
            field_options_data.add_field_option(field_option['option'], field_option['id'])
        
        field_service.save_field(
            enabled=field_instance.enabled,
            label_name=field_instance.label_name,
            order=field_instance.order,
            is_unique=field_instance.is_unique,
            field_is_hidden=field_instance.field_is_hidden,
            label_is_hidden=field_instance.label_is_hidden,
            placeholder=field_instance.placeholder,
            required=field_instance.required,
            section=field_instance.form,
            form_field_as_option=field_instance.form_field_as_option,
            formula_configuration=field_instance.formula_configuration,
            date_configuration_auto_create=field_instance.date_configuration_auto_create,
            date_configuration_auto_update=field_instance.date_configuration_auto_update,
            number_configuration_number_format_type=field_instance.number_configuration_number_format_type,
            date_configuration_date_format_type=field_instance.date_configuration_date_format_type,
            period_configuration_period_interval_type=field_instance.period_configuration_period_interval_type,
            field_type=field_instance.type,
            field_options_data=field_options_data,
            instance=field_instance
        )

        return instances


class KanbanDimensionSerializer(serializers.ModelSerializer):
    """
    Serializer used for loading the dimension phases to the user. Dimension phases is just a fancy word for FieldOption
    """
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = FieldOptions
        list_serializer_class = KanbanDimensionListSerializer
        fields = ('id','option')


class KanbanCollapsedDimensionListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        print(validated_data)
        collapsed_field_option_ids = [kanban_collapsed_dimension.get('field_option_id') for kanban_collapsed_dimension in validated_data]
        kanban_service = KanbanService(user_id=self.context['user_id'], company_id=self.context['company_id'], form_name=self.context['form_name'])
        kanban_service.save_collapsed_dimension_phases(collapsed_field_option_ids)
        return instance


class KanbanCollapsedDimensionSerializer(serializers.ModelSerializer):
    field_option_id = serializers.IntegerField()
    
    class Meta:
        model = KanbanCollapsedOption
        list_serializer_class = KanbanCollapsedDimensionListSerializer
        fields = ('field_option_id',)


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
        """
        What we do here is prepare the data to change the rows of the kanban.

        What you notice right away is that what we actually do is build a formulary data on the fly changing
        only the value of the FormValue that was changed and then sending it to the FormularyDataService. 
        We do this because we can reuse all of the validation logic of this service without the need to redo it again.
        """
        form_value_to_change = FormValue.kanban_.form_value_by_form_value_id(int(data['form_value_id']))
        sections = DynamicForm.kanban_.sections_data_by_depends_on_id(form_value_to_change.form.depends_on.id)
        formulary_data = self.formulary_data_service.add_formulary_data(form_value_to_change.form.depends_on.id)
        for section in sections:
            section_data = formulary_data.add_section_data(section_id=section.form.id, section_data_id=section.id)
            section_field_values = FormValue.kanban_.form_values_by_dynamic_form_id(section.id)
            for field_value in section_field_values:
                # The data we use is the represented data since it will reformat again when saving.
                representation_service = RepresentationService(
                    field_value.field_type.type, 
                    field_value.date_configuration_date_format_type, 
                    field_value.number_configuration_number_format_type, 
                    field_value.form_field_as_option, 
                    True
                )
                value = representation_service.representation(field_value.value)
                value = data['new_value'] if field_value.id == form_value_to_change.id else value
                section_data.add_field_value(field_value.field.id, field_value.field.name, value, field_value.id)
        if self.formulary_data_service.is_valid():
            return data
        else:
            raise serializers.ValidationError(detail=self.formulary_data_service.errors)
        

    def save(self):
        instance = self.formulary_data_service.save()
        return instance