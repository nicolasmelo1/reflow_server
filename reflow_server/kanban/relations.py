from rest_framework import serializers

from reflow_server.formulary.models import Field
from reflow_server.kanban.models import KanbanCardField


class KanbanFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    label_name = serializers.CharField(required=False)
    type_id = serializers.IntegerField(required=False)

    class Meta:
        model = Field
        fields = ('id', 'name', 'label_name', 'type_id')


class KanbanCardFieldRelation(serializers.ModelSerializer):
    field = KanbanFieldsRelation()

    class Meta:
        model = KanbanCardField
        fields = ('field',)
