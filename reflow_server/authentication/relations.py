from rest_framework import serializers

from reflow_server.formulary.models import OptionAccessedBy, FormAccessedBy, \
    Field, FieldOptions, Form
from reflow_server.billing.models import CompanyBilling


class OptionAccessedByRelation(serializers.ModelSerializer):
    field_option_id = serializers.IntegerField()    
    
    class Meta:
        model = OptionAccessedBy
        fields = ('field_option_id',)


class FormAccessedByRelation(serializers.ModelSerializer):
    form_id = serializers.IntegerField()
    
    class Meta:
        model = FormAccessedBy
        fields = ('form_id',)


class FieldOptionRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = FieldOptions
        fields = ('id', 'option')


class FieldTypeOptionOnlyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = Field.objects.filter(form__depends_on=data.core_filters['form'], type__type='option')
        return super(FieldTypeOptionOnlyListSerializer, self).to_representation(data)


class FormularyFieldsOptionsRelation(serializers.ModelSerializer):
    field_option = FieldOptionRelation(many=True)

    class Meta:
        model = Field
        list_serializer_class = FieldTypeOptionOnlyListSerializer
        fields = ('enabled', 'label_name', 'field_option')


class FormularyOptionsListSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        instance = instance.filter(depends_on__isnull=True)
        return super(FormularyOptionsListSerializer, self).to_representation(instance)


class FormularyOptionsRelation(serializers.ModelSerializer):
    form_fields = FormularyFieldsOptionsRelation(many=True)

    class Meta:
        model = Form
        list_serializer_class = FormularyOptionsListSerializer
        fields = ('id', 'label_name', 'enabled', 'form_fields')

    
class CompanyBillingRelation(serializers.ModelSerializer):
    class Meta:
        model = CompanyBilling
        fields = ('is_supercompany', 'is_paying_company')