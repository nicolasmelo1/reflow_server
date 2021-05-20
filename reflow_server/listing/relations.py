from rest_framework import serializers

from reflow_server.formulary.models import Field


class ListingHeaderFieldsRelation(serializers.ModelSerializer):
    id = serializers.IntegerField()
    conditional = serializers.SerializerMethodField()

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
