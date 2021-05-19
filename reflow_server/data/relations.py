from django.db.models import Case, When

from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.data.models import FormValue, DynamicForm


class FieldValueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(field__enabled=True)
        return super(FieldValueListSerializer, self).to_representation(data)


class FieldValueRelation(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    field_name = serializers.CharField(source='field.name')
    field_id = serializers.IntegerField()
    value = ValueField(source='*', allow_blank=True, load_ids=True)

    class Meta:
        model = FormValue
        list_serializer_class = FieldValueListSerializer
        fields = ('id', 'value', 'field_id', 'field_name')


class SectionDataListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(form__enabled=True).order_by('-id')
        return super(SectionDataListSerializer, self).to_representation(data)


class SectionDataRelation(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    form_id = serializers.CharField()
    uuid = serializers.UUIDField()
    dynamic_form_value = FieldValueRelation(many=True)

    class Meta:
        model = DynamicForm
        list_serializer_class = SectionDataListSerializer
        fields = ('id', 'form_id', 'uuid', 'dynamic_form_value')


class FilteredFormularyValueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context.get('fields', None):
            # this prevents us from retrieving the same form_value_id twice
            new_data = []
            retrieved_form_value_ids = []
            for field_id in self.context.get('fields'):
                for form_value in self.context['form_values_reference'].get(data.core_filters['form'].id, {}).get(int(field_id), []):
                    if form_value.id not in retrieved_form_value_ids:
                        retrieved_form_value_ids.append(form_value.id)
                        new_data.append(form_value)
            data = new_data
        else:
            data = [form_value for field_values in self.context['form_values_reference'].get(data.core_filters['form'].id, {}).values() for form_value in field_values]
        return super(FilteredFormularyValueListSerializer, self).to_representation(data)


class FormularyValueRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    field_name = serializers.CharField(source='field.name')
    value = ValueField(source="*")

    class Meta:
        model = FormValue
        list_serializer_class = FilteredFormularyValueListSerializer
        fields = ('id', 'value', 'field_id', 'field_name')
