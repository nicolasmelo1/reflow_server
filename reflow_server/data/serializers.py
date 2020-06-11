from rest_framework import serializers

from reflow_server.data.services import FormularyDataService
from reflow_server.data.relations import SectionDataRelation, FormularyValueRelation
from reflow_server.data.models import DynamicForm


class FormDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    depends_on_dynamic_form = SectionDataRelation(many=True)

    def __init__(self, user_id, company_id, form_name, form_data_id=None, duplicate=False, **kwargs):
        self.form_data_id = form_data_id
        self.duplicate = False
        self.formulary_service = FormularyDataService(user_id, company_id, form_name)
        super(FormDataSerializer, self).__init__(**kwargs)

    def validate(self, data):
        formulary_data = self.formulary_service.add_formulary_data(self.form_data_id, duplicate=self.duplicate)
        for section in data['depends_on_dynamic_form']:
            section_data = formulary_data.add_section_data(section_id=section['form_id'], section_data_id=section['id'])
            for field in section['dynamic_form_value']:
                section_data.add_field_value(field['field']['name'], field['value'], field['id'])

        if self.formulary_service.is_valid():
            return data
        else:
            raise serializers.ValidationError(detail=self.formulary_service.errors)
        
    def save(self, files):
        instance = self.formulary_service.save(files)
        return instance
    
    class Meta:
        model = DynamicForm
        fields = ('id', 'depends_on_dynamic_form',)


class DataSerializer(serializers.ModelSerializer):
    dynamic_form_value = FormularyValueRelation(many=True)

    class Meta:
        model = DynamicForm
        fields = ('id', 'user', 'dynamic_form_value')