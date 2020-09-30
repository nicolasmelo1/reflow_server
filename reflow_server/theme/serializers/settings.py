from rest_framework import serializers

from reflow_server.theme.models import Theme


class ThemeSettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    form_ids = serializers.ListField(allow_empty=True)

    class Meta:
        model = Theme
        fields = ('id', 'display_name', 'theme_type', 'description', 'form_ids', 'is_public')
