from rest_framework import serializers

from reflow_server.theme.models import Theme


class ThemeSettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Theme
        fields = ('id', 'display_name', 'theme_type', 'description', 'is_public')
