from django.db.models import Case, When

from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.formulary.models import Field, FormValue, DynamicForm, Form


class ListingHeaderFieldsRelation(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'label_name', 'name', 'type', 'user_selected')


class ExtractFormValueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        sections = list(DynamicForm.objects.filter(company_id=self.context['company_id'], depends_on=data.core_filters['form'].id).values_list('id', flat=True))
        if 'fields' in self.context and self.context['fields']:
            order = Case(*[When(field_id=value, then=pos) for pos, value in enumerate(self.context['fields'])])
            data = FormValue.objects.filter(company_id=self.context['company_id'], form_id__in=sections, field_id__in=self.context['fields']).order_by(order)
        else:
            data = FormValue.objects.filter(company_id=self.context['company_id'], form_id__in=sections)
        return super(ExtractFormValueListSerializer, self).to_representation(data)


class ExtractFormValueRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    field_name = serializers.CharField(source='field.name')
    value = ValueField(source='*')

    class Meta:
        model = FormValue
        list_serializer_class = ExtractFormValueListSerializer
        fields = ('id', 'value', 'field_id', 'field_name')


class ExtractSectionFieldListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(enabled=True)
        return super(ExtractSectionFieldListSerializer, self).to_representation(data)


class ExtractSectionFieldRelation(serializers.ModelSerializer):
    class Meta:
        model = Field
        list_serializer_class = ExtractSectionFieldListSerializer
        exclude = ('created_at', 'updated_at')


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
        fields = ('id', 'label_name', 'form_type', 'form_fields')
