from rest_framework import serializers

from reflow_server.formulary.models import Field
from reflow_server.kanban.models import KanbanCardField


class GetKanbanFieldsRelation(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('id', 'name', 'label_name')


class KanbanCardFieldRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(source='field.id')
    label = serializers.CharField(source='field.label_name', allow_null=True, allow_blank=True, required=False)

    class Meta:
        model = KanbanCardField
        fields = ('id', 'label')