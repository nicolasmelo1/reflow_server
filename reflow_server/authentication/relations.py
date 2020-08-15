from rest_framework import serializers

from reflow_server.formulary.models import OptionAccessedBy, FormAccessedBy, \
    Field, FieldOptions, Form


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
        data = data.filter(type__type='option')
        return super(FieldTypeOptionOnlyListSerializer, self).to_representation(data)


class FormularyFieldsOptionsRelation(serializers.ModelSerializer):
    field_option = FieldOptionRelation(many=True)

    class Meta:
        model = Field
        list_serializer_class = FieldTypeOptionOnlyListSerializer
        fields = ('enabled', 'label_name', 'field_option')


class FormularyOptionsRelation(serializers.ModelSerializer):
    form_fields = FormularyFieldsOptionsRelation(many=True)

    class Meta:
        model = Form
        fields = ('id', 'label_name', 'enabled', 'form_fields')