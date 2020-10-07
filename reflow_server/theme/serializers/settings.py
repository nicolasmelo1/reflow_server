from rest_framework import serializers

from reflow_server.theme.models import Theme
from reflow_server.formulary.models import Form
from reflow_server.theme.services import ThemeService

class ThemeSettingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)
    description = serializers.CharField(allow_null=False, allow_blank=False, error_messages={'invalid': 'invalid', 'blank': 'blank'})
    display_name = serializers.CharField(allow_null=False, allow_blank=False, error_messages={'invalid': 'invalid', 'blank': 'blank'})
    form_ids = serializers.ListField(allow_empty=True, default=[])
    
    def validate(self, data):
        if not self.instance and not data.get('form_ids', []):
            raise serializers.ValidationError(detail={'detail': 'forms_not_defined', 'reason': 'form_ids_should_be_defined_when_creating'})
        return data
    
    def create(self, validated_data):
        instance = ThemeService.update_or_create_theme(
            validated_data.get('theme_type').id,
            validated_data.get('display_name', None),
            validated_data.get('is_public', False),
            validated_data.get('description', False),
            self.context.get('user_id', None),
            self.context.get('company_id', None),
            validated_data.get('form_ids', [])
        )
        return instance

    def update(self, instance, validated_data):
        instance = ThemeService.update_or_create_theme(
            validated_data.get('theme_type').id,
            validated_data.get('display_name', None),
            validated_data.get('is_public', False),
            validated_data.get('description', False),
            self.context.get('user_id', None),
            self.context.get('company_id', None),
            validated_data.get('form_ids', []),
            instance.id
        )
        return instance

    class Meta:
        model = Theme
        fields = ('id', 'display_name', 'theme_type', 'description', 'form_ids', 'is_public')


class FormularyOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Form
        fields = ('id', 'label_name')