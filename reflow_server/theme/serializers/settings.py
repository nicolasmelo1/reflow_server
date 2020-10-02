from rest_framework import serializers

from reflow_server.theme.models import Theme
from reflow_server.formulary.models import Form


class ThemeSettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    form_ids = serializers.ListField(allow_empty=True, default=[])

    class Meta:
        model = Theme
        fields = ('id', 'display_name', 'theme_type', 'description', 'form_ids', 'is_public')


class FormularyOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Form
        fields = ('id', 'label_name')