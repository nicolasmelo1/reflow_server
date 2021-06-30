from rest_framework import serializers

from reflow_server.formulary.services.fields import FieldService
from reflow_server.formulary.models import Field
from reflow_server.kanban.models import KanbanCardField

from collections import OrderedDict


class KanbanFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    label_name = serializers.CharField(required=False)
    type_id = serializers.SerializerMethodField()

    def get_type_id(self, obj):
        if isinstance(obj, OrderedDict):
            obj = Field.objects.filter(id=obj['id']).first()
        
        field_type = FieldService.retrieve_actual_field_type_for_field(obj.id, obj.type)
        if field_type:
            return field_type.id
        else:
            return None
        
    class Meta:
        model = Field
        fields = ('id', 'name', 'label_name', 'type_id')


class KanbanCardFieldRelation(serializers.ModelSerializer):
    field = KanbanFieldsRelation()

    class Meta:
        model = KanbanCardField
        fields = ('field',)
