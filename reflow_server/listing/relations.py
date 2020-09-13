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
        sections = list(
            DynamicForm.listing_.dynamic_form_ids_by_depends_on_id_and_company_id( 
                data.core_filters['form'].id,
                self.context['company_id']
            )
        )
        if 'fields' in self.context and self.context['fields']:
            data = FormValue.listing_.form_values_by_company_id_and_form_ids_and_field_ids_ordered(self.context['company_id'], sections, self.context['fields'])
        else:
            data = FormValue.listing_.form_values_by_company_id_and_form_ids(self.context['company_id'], sections)
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
