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
    value = ValueField(source='*', allow_blank=True, load_ids=True)

    class Meta:
        model = FormValue
        list_serializer_class = FieldValueListSerializer
        fields = ('id', 'value', 'field_name')


class SectionDataListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(form__enabled=True).order_by('-id')
        return super(SectionDataListSerializer, self).to_representation(data)


class SectionDataRelation(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    form_id = serializers.CharField()
    dynamic_form_value = FieldValueRelation(many=True)

    class Meta:
        model = DynamicForm
        list_serializer_class = SectionDataListSerializer
        fields = ('id', 'form_id', 'dynamic_form_value')


class FilteredFormularyValueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        sections = list(DynamicForm.objects.filter(
            company_id=self.context['company_id'], 
            depends_on=data.core_filters['form'].id
        ).values_list('id', flat=True))
        if self.context.get('fields', None):
            order = Case(*[When(field_id=value, then=pos) for pos, value in enumerate(self.context['fields'])])
            data = FormValue.objects.filter(
                company_id=self.context['company_id'], 
                form_id__in=sections, 
                field_id__in=self.context['fields']
            ).order_by(order)
        else:
            data = FormValue.objects.filter(
                company_id=self.context['company_id'], 
                form_id__in=sections
            )
        return super(FilteredFormularyValueListSerializer, self).to_representation(data)


class FormularyValueRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    field_name = serializers.CharField(source='field.name')
    value = ValueField(source='*')

    class Meta:
        model = FormValue
        list_serializer_class = FilteredFormularyValueListSerializer
        fields = ('id', 'value', 'field_id', 'field_name')
