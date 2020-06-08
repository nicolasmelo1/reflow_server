from rest_framework import serializers

from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.relations import SectionDataSerialiser
from reflow_server.formulary.models import DynamicForm


class FormDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    depends_on_dynamic_form = SectionDataSerialiser(many=True)

    def __init__(self, user_id, company_id, form_name, form_data_id=None, **kwargs):
        self.form_data_id = form_data_id
        self.formulary_service = FormularyService(user_id, company_id, form_name)
        super(FormDataSerializer, self).__init__(**kwargs)

    def validate(self, data):
        self.form_data_id = form_data_id
        formulary_data = self.formulary_service.add_formulary_data(self.form_data_id)
        for section in data['depends_on_dynamic_form']:
            section_data = formulary_data.add_section_data(section_id=section['form_id'], section_data_id=section['id'])
            for field in section['dynamic_form_value']:
                section_data.add_field_value(field['field']['name'], field['value'], field['id'])

        if self.formulary_service.is_valid():
            return data
        else:
            raise serializers.ValidationError(detail=self.formulary_service.errors)
        
    def save(self):
        instance = self.formulary_service.save()
        return instance
    
    class Meta:
        model = DynamicForm
        fields = ('id', 'depends_on_dynamic_form',)
