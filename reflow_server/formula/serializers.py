from rest_framework import serializers


class FormulaSerializer(serializers.Serializer):
    formula = serializers.CharField(allow_blank=True, required=True)
    variable_ids = serializers.ListField()