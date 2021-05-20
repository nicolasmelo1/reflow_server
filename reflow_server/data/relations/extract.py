from rest_framework import serializers

from reflow_server.formulary.models import Field, Form


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
