from rest_framework import serializers

from reflow_server.formulary.models import Field
from reflow_server.kanban.models import KanbanCardField


class GetKanbanFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()
    
    class Meta:
        model = Field
        fields = ('id', 'name', 'label_name', 'type')


class KanbanCardFieldListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('id')
        return super(KanbanCardFieldListSerializer, self).to_representation(data)


class KanbanCardFieldRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(source='field.id')
    label = serializers.CharField(source='field.label_name', allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = KanbanCardField
        list_serializer_class = KanbanCardFieldListSerializer
        fields = ('id', 'label')