from rest_framework import serializers

from reflow_server.formulary.models import Field
from reflow_server.data.models import FormValue


class ListingHeaderFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()
    type = serializers.SerializerMethodField()
    conditional = serializers.SerializerMethodField()

    def get_type(self, obj):
        if obj.type.type == 'formula':
            try:
                latest_form_value = FormValue.objects.filter(field_id=obj.id).latest('updated_at')         
                if latest_form_value:   
                    return latest_form_value.field_type_id
            except:
                pass
        return obj.type_id
    
    def get_conditional(self, obj):
        if obj.form.conditional_on_field and obj.form.conditional_type:
            return {
                'conditional_field_label_name': obj.form.conditional_on_field.label_name,
                'conditional_type': obj.form.conditional_type.type,
                'conditional_value': obj.form.conditional_value
            }
        else:
            return None

    class Meta:
        model = Field
        fields = ('id', 'label_name', 'name', 'type', 'conditional')
