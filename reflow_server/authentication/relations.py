from rest_framework import serializers

from reflow_server.authentication.models import APIAccessToken
from reflow_server.formulary.models import OptionAccessedBy, FormAccessedBy, \
    Field, FieldOptions, Form, UserAccessedBy
from reflow_server.billing.models import CompanyBilling


class HasAPIAccessKeyRelation(serializers.BooleanField):
    def to_representation(self, value):
        has_access_key = APIAccessToken.authentication_.exists_by_user_id_and_company_id(
            value, 
            self.context.get('company_id', None)
        )
        return super().to_representation(has_access_key)


class UserAccessedByRelation(serializers.ModelSerializer):
    user_option_id = serializers.IntegerField()    
    field_id = serializers.IntegerField()

    class Meta:
        model = UserAccessedBy
        fields = ('user_option_id', 'field_id')


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
        data = Field.objects.filter(form__depends_on=data.core_filters['form'], type__type__in=['option', 'multi_option', 'user'])
        return super(FieldTypeOptionOnlyListSerializer, self).to_representation(data)


class FormularyFieldsOptionsRelation(serializers.ModelSerializer):
    field_option = FieldOptionRelation(many=True)

    class Meta:
        model = Field
        list_serializer_class = FieldTypeOptionOnlyListSerializer
        fields = ('id', 'enabled', 'label_name', 'type', 'field_option')


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