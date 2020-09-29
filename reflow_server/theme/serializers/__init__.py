from rest_framework import serializers

from reflow_server.theme.models import Theme, ThemeForm
from reflow_server.theme.relations import ThemeSectionRelation


class ThemeFormularyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(depends_on__isnull=True).order_by('order')
        return super(ThemeFormularyListSerializer, self).to_representation(data)


class ThemeFormularySerializer(serializers.ModelSerializer):
    label_name = serializers.CharField(allow_null=True, allow_blank=True)
    depends_on_theme_form = ThemeSectionRelation(many=True)

    def __init__(self, is_loading_formulary=False, *args, **kwargs):
        """
        Loads the used for loading the formulary data and presenting it to the user. It has two main applications:
        1 - You want only to load the most basic data of the formulary, it's fields and sections are not necessary
        2 - You want to load the hole formulary with it's fields and sections.

        Args:
            is_loading_formulary (bool, optional): If you want to use this serializer for LOADING the formulary data
            you set this to true. When set to true the sections and fields of the theme will be loaded, otherwise
            they are ignored. Defaults to False.
        """
        super(ThemeFormularySerializer, self).__init__(*args, **kwargs)
        
        if not is_loading_formulary:
            self.fields.pop('depends_on_theme_form')


    class Meta:
        model = ThemeForm
        list_serializer_class = ThemeFormularyListSerializer
        fields = ('id', 'form_name', 'label_name', 'depends_on_theme_form')


class ThemeSerializer(serializers.ModelSerializer):
    """
    Serializer responsible for retrieving all of the themes to the user, it holds the data that the user needs to see
    about the theme before selecting the theme.

    You will notice that this does not hold the ThemeForm data, if it held this serializer would be to costly
    to load.
    """
    id = serializers.IntegerField(allow_null=True)
    theme_form = ThemeFormularySerializer(many=True)
    theme_type = serializers.CharField(source='theme_type.name', default='')
    user = serializers.CharField(source='user.first_name', allow_blank=True, allow_null=False, required=False)
    description = serializers.CharField(max_length=500)

    class Meta:
        model = Theme
        fields = ('id', 'display_name', 'theme_type', 'user', 'description', 'is_public', 'theme_form')
