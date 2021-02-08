from rest_framework import serializers

from reflow_server.data.services import FormularyDataService
from reflow_server.data.relations import SectionDataRelation, FormularyValueRelation
from reflow_server.data.models import DynamicForm


class FormDataSerializer(serializers.ModelSerializer):
    """
    Serializer used from loading and saving the data of a single and unique formulary data.
    Diferently from DataSerializer, this serializer actually cares about the sections, so it formats
    the data in a way it's easier to differentiate. From which section this data is from.

    Args:
        user_id (int): The id of the user who is updating or saving the data
        company_id (int): the id from the company this data is from
        form_name (int): From which formulary this formulary data is from, we just need the name here.
        form_data_id (int, optional): Only if you are updating or duplicating an existing formulary. Defaults to None.
        duplicate (bool, optional): Only needed if you are duplicating a formulary. Defaults to False.
    """
    id = serializers.IntegerField(allow_null=True, required=False)
    depends_on_dynamic_form = SectionDataRelation(many=True)

    def __init__(self, user_id, company_id, form_name, form_data_id=None, duplicate=False, **kwargs):
        self.form_data_id = form_data_id
        self.duplicate = duplicate
        self.formulary_service = FormularyDataService(user_id, company_id, form_name)
        super(FormDataSerializer, self).__init__(**kwargs)

    def validate(self, data):
        formulary_data = self.formulary_service.add_formulary_data(self.form_data_id, duplicate=self.duplicate)
        for section in data['depends_on_dynamic_form']:
            section_data = formulary_data.add_section_data(section_id=section['form_id'], section_data_id=section['id'])
            for field in section['dynamic_form_value']:
                section_data.add_field_value(field['field_id'], field['field']['name'], field['value'], field['id'])
        if self.formulary_service.is_valid():
            return data
        else:
            raise serializers.ValidationError(detail=self.formulary_service.errors)
        
    def save(self, files={}):
        instance = self.formulary_service.save()
        return instance
    
    class Meta:
        model = DynamicForm
        fields = ('id', 'depends_on_dynamic_form',)


class DataSerializer(serializers.ModelSerializer):
    """
    Serializer from retrieving the data for listing and kanban visualizations, and probably many more
    visualizations to come. This serializer is often used just to read the data, but not saving.
    This is because we format the data completly ignoring the sections and caring just about the values.

    Context Args:
        fields (optional, list(int)) -- list of field ids to use, this way this doesn't retrieve the data from
                                       all of the fields, but only a small portion of them. Default as None.
        company_id (int) -- We need this to retrieve the correct data when loading the formulary
    """
    dynamic_form_value = FormularyValueRelation(many=True)

    class Meta:
        model = DynamicForm
        fields = ('id', 'dynamic_form_value')