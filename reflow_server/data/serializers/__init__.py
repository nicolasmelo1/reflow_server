from rest_framework import serializers

from reflow_server.data.services import FormularyDataService
from reflow_server.data.relations import SectionDataRelation, FormularyValueRelation
from reflow_server.data.models import DynamicForm, FormValue
from reflow_server.data.services import RepresentationService
from reflow_server.core.relations import ValueField

############################################################################################
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
    uuid = serializers.UUIDField()
    depends_on_dynamic_form = SectionDataRelation(many=True)

    def __init__(self, user_id, company_id, form_name, duplicate=False, public_access_key=None, **kwargs):
        self.duplicate = duplicate
        self.formulary_service = FormularyDataService(user_id, company_id, form_name, public_access_key=public_access_key)
        super(FormDataSerializer, self).__init__(**kwargs)
    # ------------------------------------------------------------------------------------------
    def validate(self, data):
        formulary_data = self.formulary_service.add_formulary_data(
            data['uuid'],
            self.instance.id if self.instance else None, 
            duplicate=self.duplicate
        )
        for section in data['depends_on_dynamic_form']:
            section_data = formulary_data.add_section_data(
                section_id=section['form_id'], 
                uuid=section['uuid'], 
                section_data_id=section['id']
            )
            for field in section['dynamic_form_value']:
                section_data.add_field_value(field['field_id'], field['field']['name'], field['value'], field['id'])
        if self.formulary_service.is_valid():
            return data
        else:
            raise serializers.ValidationError(detail=self.formulary_service.errors)
    # ------------------------------------------------------------------------------------------
    def save(self):
        instance = self.formulary_service.save()
        return instance
    
    class Meta:
        model = DynamicForm
        fields = ('id', 'uuid', 'depends_on_dynamic_form')


############################################################################################
class FieldValueSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    field_name = serializers.CharField(source='field.name')
    field_id = serializers.IntegerField()
    value = ValueField(source='*', allow_blank=True, load_ids=True)

    class Meta:
        model = FormValue
        fields = ('id', 'value', 'field_id', 'field_name')

class SectionSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    form_id = serializers.CharField()
    uuid = serializers.UUIDField()
    dynamic_form_value = FieldValueSerializer(many=True)

    class Meta:
        model = DynamicForm
        fields = ('id', 'form_id', 'uuid', 'dynamic_form_value')

class DataSerializer(serializers.Serializer):
    """
    Serializer from retrieving the data for listing and kanban visualizations, and probably many more
    visualizations to come. This serializer is often used just to read the data, but not saving.
    This is because we format the data completly ignoring the sections and caring just about the values.
    """
    dynamic_form_value = FormularyValueRelation(many=True)

    @staticmethod
    def retrieve_data(main_form_ids, company_id, field_ids=[]):
        """
        So you might ask yourself:
        "WTF, why retrieve data like that and not using ModelSerializer like a normal person?"

        This happened in May of 2021: We had performance issues when retrieving data using ModelSerializer, what happened is that
        when we create a field like:

        `field_name = serializers.CharField(source='field.name')`
        
        what Django does to retrieve this data is a SELECT query on 'field' table like 
        SELECT * FROM "field" WHERE "field"."id" = %s LIMIT 21

        The problem is then elevated to 2 when we use the reflow_server.core.relations.ValueField custom field.
        
        So to get a single related attribute data what Django does is make a query for the hole row data, as you might already know retrieve a data
        for a single field of the table is better than retrieve the hole data.

        But the problem is: this was happening for EVERY FORM_VALUE, and a single Data in reflow is composed of MANY form_values.
        So to get few saved DynamicForm instances it was taking ages because it needed to do so many queries because and only because of those relations.

        To simplify the number of queries we made the serializer a simple serializer, so the only thing Django Rest Framework has to do
        is convert a dict to a object and then to a dict again, yes, this causes an overhead, but we can still guarantee a particular serialization
        and deserialization for the data, and since this serialization is not I/O bound it takes way less than it would be if we needed to make lots of queries.

        TL.DR:
        What happens is that when you retrieve a related attribute in django like `form_value.field.name`, django makes a query to retrieve all of the fields of the 
        'field' table. The query made is not optimized and it actually doesn't need to exist, so what we do is minimize the number of queries made using
        a simple serializer and not a ModelSerializer.

        Args:
            main_form_ids (list[int]): DynamicForm instances ids used to retrieve the FormValue of those.
            company_id (int): The company id the user is logged in
            field_ids (list[int], optional): List of Field instances ids, if you want to retrieve the data for some particular fields you use this, this will optimize the query. Defaults to [].

        Returns:
            list[{'dynamic_form_value': dict}]: Returns a list of dicts where each dict is a DynamicForm and the only key in each dict is the 'dynamic_form_value'
                                                containing each FormValue.
        """
        data = {}
        form_values = FormValue.data_.form_value_id_field_name_form_field_as_option_id_number_format_id_date_format_id_field_type_value_field_id_and_form_depends_on_by_main_form_ids_company_id_and_field_ids(
            main_form_ids,
            company_id,
            field_ids
        )
        for form_value in form_values:
            depends_on_id = form_value['form__depends_on_id']
            representation = RepresentationService(
                form_value['field_type__type'], 
                form_value['date_configuration_date_format_type_id'], 
                form_value['number_configuration_number_format_type_id'], 
                form_value['form_field_as_option_id'], 
                False
            )
            form_value_data = {
                'id': form_value['id'],
                'field_name': form_value['field__name'],
                'field_id': form_value['field_id'],
                'value': representation.representation(form_value['value'])
            }
            if depends_on_id:
                if data.get(depends_on_id):
                    data[depends_on_id]['dynamic_form_value'].append(form_value_data)
                else:
                    data[depends_on_id] = {
                        'dynamic_form_value': []
                    }
                    data[depends_on_id]['dynamic_form_value'].append(form_value_data)
        
        return data.values()
        