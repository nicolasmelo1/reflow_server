from django.db.models import Case, When

from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.data.models import FormValue, DynamicForm
from reflow_server.formulary.models import Field, Form


class ListingHeaderFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()
    conditional = serializers.SerializerMethodField()

    def get_conditional(self, obj):
        if obj.form.conditional_on_field and obj.form.conditional_type:
            return {
                'conditional_field_label_name': obj.form.conditional_on_field.label_name,
                'conditional_type': obj.form.conditional_type.type,
                'conditional_value': obj.form.conditional_value
            }
        else:
            return None

    class Meta:
        model = Field
        fields = ('id', 'label_name', 'name', 'type', 'conditional')


class ExtractFormValueListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context.get('fields', None):
            # this prevents us from retrieving the same form_value_id twice
            """
            new_data = []
            retrieved_form_value_ids = []
            for field_id in self.context.get('fields'):
                for form_value in self.context['form_values_reference'].get(data.core_filters['form'].id, {}).get(int(field_id), []):
                    if form_value.id not in retrieved_form_value_ids:
                        retrieved_form_value_ids.append(form_value.id)
                        new_data.append(form_value)
            data = new_data
            """
            data = FormValue.objects.filter(form__depends_on_id=data.core_filters['form'].id, field_id__in=self.context.get('fields'))
        else:
            data = FormValue.objects.filter(form__depends_on_id=data.core_filters['form'].id)
            #data = [form_value for field_values in self.context['form_values_reference'].get(data.core_filters['form'].id, {}).values() for form_value in field_values]
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
