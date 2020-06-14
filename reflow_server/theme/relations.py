from rest_framework import serializers

from reflow_server.theme.models import ThemeForm, ThemeFieldOptions, \
    ThemeField


class ThemeFieldOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = ThemeFieldOptions
        fields = ('option',)


class ThemeFieldRelation(serializers.ModelSerializer):
    theme_field_option = ThemeFieldOptionRelation(many=True)

    class Meta:
        model = ThemeField
        exclude = ('created_at', 'updated_at')


class ThemeSectionRelation(serializers.ModelSerializer):
    conditional_on_theme_field = serializers.CharField(source='conditional_on_theme_field.name', read_only=True)
    conditional_type_type = serializers.CharField(source='conditional_type.type', read_only=True)
    form_type = serializers.CharField(source='type.type', read_only=True)
    theme_form_fields = ThemeFieldRelation(many=True)

    class Meta:
        model = ThemeForm
        fields = ('id',
                  'label_name',
                  'form_type',
                  'conditional_on_theme_field',
                  'conditional_type_type',
                  'conditional_value',
                  'theme_form_fields')