from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.formulary.models import FormValue, DynamicForm


class FieldValueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(field__enabled=True)
        return super(FieldValueListSerializer, self).to_representation(data)


class FieldValueSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    field_name = serializers.CharField(source='field.name')
    value = ValueField(source='*', allow_blank=True, load_ids=True, max_length=2000)

    class Meta:
        model = FormValue
        list_serializer_class = FieldValueListSerializer
        fields = ('id', 'value', 'field_name')


class SectionDataListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(form__enabled=True).order_by('-id')
        return super(SectionDataListSerializer, self).to_representation(data)


class SectionDataSerialiser(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    form_id = serializers.CharField()
    dynamic_form_value = FieldValueSerializer(many=True)

    class Meta:
        model = DynamicForm
        list_serializer_class = SectionDataListSerializer
        fields = ('id', 'form_id', 'dynamic_form_value')