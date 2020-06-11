from rest_framework import serializers

from reflow_server.formulary.models import Form, Field, OptionAccessedBy, FieldOptions, FormAccessedBy


class FilteredFieldOptionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(id__in=OptionAccessedBy.objects.filter(user_id=self.context['user_id']) \
                                   .values_list('field_option_id', flat=True)).order_by('id')
        return super(FilteredFieldOptionListSerializer, self).to_representation(data)


class FieldOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = FieldOptions
        list_serializer_class = FilteredFieldOptionListSerializer
        fields = ('option',)


class FormFieldAsOptionRelation(serializers.ModelSerializer):
    form_name = serializers.CharField(source='form.depends_on.form_name')

    class Meta:
        model = Field
        fields = ('form_name',)


class FilteredFieldsListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(enabled=True)
        return super(FilteredFieldsListSerializer, self).to_representation(data)


class FormFieldRelation(serializers.ModelSerializer):
    form_field_as_option = FormFieldAsOptionRelation()
    field_option = FieldOptionRelation(many=True)

    class Meta:
        model = Field
        list_serializer_class = FilteredFieldsListSerializer
        exclude = ('created_at', 'updated_at')


class FilteredSectionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(enabled=True)
        return super(FilteredSectionListSerializer, self).to_representation(data)


class SectionRelation(serializers.ModelSerializer):
    conditional_on_field_name = serializers.CharField(source='conditional_on_field.name', read_only=True)
    conditional_type_type = serializers.CharField(source='conditional_type.type', read_only=True)
    form_type = serializers.CharField(source='type.type', read_only=True)
    form_fields = FormFieldRelation(many=True)

    class Meta:
        model = Form
        list_serializer_class = FilteredSectionListSerializer
        fields = ('id',
                  'label_name',
                  'form_type',
                  'conditional_on_field_name',
                  'conditional_type_type',
                  'conditional_value',
                  'form_fields')


class FormListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        forms_accessed_by = FormAccessedBy.objects.filter(user=self.context['user_id']).values_list('form', flat=True)
        forms = data.filter(id__in=forms_accessed_by, enabled=True, depends_on__isnull=True).order_by('order')
        return super(FormListSerializer, self).to_representation(forms)


class FormRelation(serializers.ModelSerializer):
    class Meta:
        model = Form
        list_serializer_class = FormListSerializer
        exclude = ('conditional_value', 'conditional_type', 'conditional_on_field', 'depends_on')
