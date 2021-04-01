from rest_framework import serializers

from reflow_server.formulary.models import Form, Field, OptionAccessedBy, FieldOptions, FormAccessedBy, PublicAccessField, DefaultFieldValue, DefaultFieldValueAttachments
from reflow_server.formulary.services.sections import SectionService
from reflow_server.formulary.services.fields import FieldService


representation_service_cache = {}

############################################################################################
class DefaultFieldValueValue(serializers.Field):
    def to_representation(self, obj):
        from reflow_server.data.services import RepresentationService

        if obj and obj.value != '':
            cache_key = '{};{};{};{}'.format(
                obj.field.type.type, 
                obj.field.date_configuration_date_format_type_id, 
                obj.field.number_configuration_number_format_type_id, 
                obj.field.form_field_as_option_id
            )

            if representation_service_cache.get(cache_key):
                representation = representation_service_cache.get(cache_key)
            else:
                representation = RepresentationService(
                    obj.field.type.type, 
                    obj.field.date_configuration_date_format_type, 
                    obj.field.number_configuration_number_format_type, 
                    obj.field.form_field_as_option, 
                )
                representation_service_cache[cache_key] = representation
                
            represented_value = representation.representation(obj.value)

            # we need to reset the cache now and then so it doesn't take much space in our memory
            if len(representation_service_cache.keys()) > 300:
                representation_service_cache.clear()

            return represented_value
        else:
            return ''


############################################################################################
class FieldDefaultValuesRelation(serializers.ModelSerializer):
    value = DefaultFieldValueValue(source='*')

    class Meta:
        model = DefaultFieldValue
        fields = ('value', )

############################################################################################
class FilteredFieldOptionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(id__in=OptionAccessedBy.objects.filter(user_id=self.context['user_id']) \
                                   .values_list('field_option_id', flat=True)).order_by('order')
        return super(FilteredFieldOptionListSerializer, self).to_representation(data)


class FieldOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = FieldOptions
        list_serializer_class = FilteredFieldOptionListSerializer
        fields = ('option',)


############################################################################################
class FormFieldAsOptionRelation(serializers.ModelSerializer):
    form_name = serializers.CharField(source='form.depends_on.form_name')

    class Meta:
        model = Field
        fields = ('form_name',)


############################################################################################
class FilteredFieldsListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context.get('public_access_key', None):
            form_id = data.core_filters['form'].depends_on_id
            section_id = data.core_filters['form'].id
            field_service = FieldService(self.context['user_id'], self.context['company_id'], form_id)
            data = field_service.get_public_fields_from_section(self.context['public_access_key'], section_id)
        data = data.filter(enabled=True).order_by('order')
        return super(FilteredFieldsListSerializer, self).to_representation(data)


class FormFieldRelation(serializers.ModelSerializer):
    form_field_as_option = FormFieldAsOptionRelation()
    field_option = FieldOptionRelation(many=True)
    field_default_field_values = FieldDefaultValuesRelation(many=True)

    class Meta:
        model = Field
        list_serializer_class = FilteredFieldsListSerializer
        exclude = ('created_at', 'updated_at')


############################################################################################
class FilteredSectionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        if self.context.get('public_access_key', None):
            form_id = data.core_filters['depends_on'].id
            section_service = SectionService(self.context['user_id'], self.context['company_id'], form_id)
            data = section_service.get_public_sections(self.context['public_access_key'])
        data = data.filter(enabled=True).order_by('order')
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


############################################################################################
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


############################################################################################
class PublicAccessFieldRelation(serializers.ModelSerializer):
    field_id = serializers.IntegerField()
    """
    Serializer responsible for holding all of the fields that are available for public access.
    Usually used in conjuction with `PublicAccessFormSerializer`
    """
    class Meta:
        model = PublicAccessField
        fields = ('field_id',)