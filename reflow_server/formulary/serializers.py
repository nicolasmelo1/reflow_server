from rest_framework import serializers

from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.relations import SectionDataSerialiser
from reflow_server.formulary.models import DynamicForm


class FormDataSerializer(serializers.ModelSerializer):
    """
    Be careful changing this serializer and the others nested, since we need to know the data structure for 'pre_save_processor' and 'post_save_processor'.
    If you change this or one of the nested ones, be sure two check both classes after.
    """
    id = serializers.IntegerField(allow_null=True, required=False)
    depends_on_dynamic_form = SectionDataSerialiser(many=True)

    def __init__(self, user_id, company_id, form_name, **kwargs):
        self.formulary_service = FormularyService(user_id, company_id, form_name)
        super().__init__(**kwargs)

    def validate(self, data):
        formulary_data = self.formulary_service.add_formulary_data(data['id'])
        for section in data['depends_on_dynamic_form']:
            section_data = formulary_data.add_section_data(section_id=section['form_id'], section_data_id=section['id'])
            for field in section['dynamic_form_value']:
                section_data.add_field_value(field['field']['name'], field['value'], field['id'])
        if self.formulary_service.is_valid():
            return data
        else:
            raise serializers.ValidationError(detail=self.formulary_service.errors)

    class Meta:
        model = DynamicForm
        fields = ('id', 'depends_on_dynamic_form',)
