from rest_framework import serializers

from reflow_server.formulary.models import OptionAccessedBy, FormAccessedBy


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
