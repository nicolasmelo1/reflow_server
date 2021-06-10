from rest_framework import serializers

from reflow_server.formulary.models import Field
from reflow_server.kanban.models import KanbanCardField
from reflow_server.data.models import FormValue

from collections import OrderedDict


class KanbanFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    name = serializers.CharField(allow_null=True)
    label_name = serializers.CharField(required=False)
    type_id = serializers.SerializerMethodField()

    def get_type_id(self, obj):
        if isinstance(obj, OrderedDict):
            obj = Field.objects.filter(id=obj['id']).first()
        if obj.type.type == 'formula':
            latest_form_value = FormValue.objects.filter(field_id=obj.id).latest('updated_at')         
            if latest_form_value:   
                return latest_form_value.field_type_id
        return obj.type_id

    class Meta:
        model = Field
        fields = ('id', 'name', 'label_name', 'type_id')


class KanbanCardFieldRelation(serializers.ModelSerializer):
    field = KanbanFieldsRelation()

    class Meta:
        model = KanbanCardField
        fields = ('field',)
