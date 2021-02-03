from django.db.models import Case, When

from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.data.models import FormValue, DynamicForm
from reflow_server.formulary.models import Field, Form


class ListingHeaderFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = Field
        fields = ('id', 'label_name', 'name', 'type')


class ExtractFormValueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context.get('fields', None):
            data = [form_value for field_id in self.context.get('fields') for form_value in self.context['form_values_reference'][data.core_filters['form'].id].get(int(field_id), [])]
        else:
            data = [form_value for field_values in self.context['form_values_reference'][data.core_filters['form'].id].values() for form_value in field_values]
        return super(ExtractFormValueListSerializer, self).to_representation(data)


class ExtractFormValueRelation(serializers.ModelSerializer):
    value = ValueField(source='*')

    class Meta:
        model = FormValue
        list_serializer_class = ExtractFormValueListSerializer
        fields = ('value', 'field_id')


class ExtractSectionFieldListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(enabled=True)
        return super(ExtractSectionFieldListSerializer, self).to_representation(data)


class ExtractSectionFieldRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Field
        list_serializer_class = ExtractSectionFieldListSerializer
        fields = ('id', 'label_name')


class ExtractSectionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(enabled=True)
        return super(ExtractSectionListSerializer, self).to_representation(data)


class ExtractSectionRelation(serializers.ModelSerializer):
    form_type = serializers.CharField(source='type.type', read_only=True)
    form_fields = ExtractSectionFieldRelation(many=True)

    class Meta:
        model = Form
        list_serializer_class = ExtractSectionListSerializer
        fields = ('form_type', 'form_fields')
