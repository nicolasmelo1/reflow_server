from rest_framework import serializers

from reflow_server.theme.models import ThemeForm, ThemeFieldOptions, \
    ThemeField


class ThemeFieldListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('order')
        return super(ThemeFieldListSerializer, self).to_representation(data)


class ThemeFieldOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = ThemeFieldOptions
        fields = ('option',)


class ThemeFieldRelation(serializers.ModelSerializer):
    theme_field_option = ThemeFieldOptionRelation(many=True)

    class Meta:
        model = ThemeField
        list_serializer_class = ThemeFieldListSerializer
        exclude = ('created_at', 'updated_at')


class ThemeSectionListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.order_by('order')
        return super(ThemeSectionListSerializer, self).to_representation(data)


class ThemeSectionRelation(serializers.ModelSerializer):
    conditional_on_theme_field = serializers.CharField(source='conditional_on_theme_field.name', read_only=True)
    conditional_type_type = serializers.CharField(source='conditional_type.type', read_only=True)
    form_type = serializers.CharField(source='type.type', read_only=True)
    theme_form_fields = ThemeFieldRelation(many=True)

    class Meta:
        model = ThemeForm
        list_serializer_class = ThemeSectionListSerializer
        fields = ('id',
                  'label_name',
                  'form_type',
                  'conditional_on_theme_field',
                  'conditional_type_type',
                  'conditional_value',
                  'theme_form_fields')