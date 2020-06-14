from rest_framework import serializers

from reflow_server.theme.models import Theme, ThemeForm
from reflow_server.theme.relations import ThemeSectionRelation


class ThemeFormularyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(depends_on__isnull=True).order_by('id')
        return super(ThemeFormularyListSerializer, self).to_representation(data)


class ThemeFormularySerializer(serializers.ModelSerializer):
    label_name = serializers.CharField(allow_null=True, allow_blank=True)
    depends_on_theme_form = ThemeSectionRelation(many=True)

    def __init__(self, is_loading_formulary=False, *args, **kwargs):
        super(ThemeFormularySerializer, self).__init__(*args, **kwargs)
        
        if not is_loading_formulary:
            self.fields.pop('depends_on_theme_form')


    class Meta:
        model = ThemeForm
        list_serializer_class = ThemeFormularyListSerializer
        fields = ('id', 'form_name', 'label_name', 'depends_on_theme_form')


class ThemeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    theme_form = ThemeFormularySerializer(many=True)
    company_type = serializers.CharField(source='company_type.name', default='')
    user = serializers.CharField(source='user.first_name', allow_blank=True, allow_null=False, required=False)
    description = serializers.CharField(max_length=500)

    class Meta:
        model = Theme
        fields = ('id', 'display_name', 'company_type', 'user', 'description', 'is_public', 'theme_form')
