from rest_framework import serializers

from reflow_server.formulary.models import Form
from reflow_server.data.services.data.extract import DataExtractService
from reflow_server.data.models import ExtractFileData
from reflow_server.data.relations.extract import ExtractSectionRelation

############################################################################################
class ExtractDataSerializer(serializers.Serializer):
    fields = serializers.ListField(required=False, allow_empty=True, child=serializers.IntegerField())
    sort_value = serializers.ListField(required=False, allow_empty=True, child=serializers.ChoiceField(choices=['upper', 'down']))
    sort_field = serializers.ListField(required=False, allow_empty=True, child=serializers.CharField())
    search_value = serializers.ListField(required=False, allow_empty=True, child=serializers.CharField(allow_blank=True))
    search_field = serializers.ListField(required=False, allow_empty=True, child=serializers.CharField())
    search_exact = serializers.ListField(required=False, allow_empty=True, child=serializers.ChoiceField(choices=['0', '1']))
    format = serializers.ChoiceField(choices=['xlsx', 'csv'])
    from_date = serializers.CharField()
    to_date = serializers.CharField()
    # ------------------------------------------------------------------------------------------
    def __init__(self, user_id, company_id, form_name, *args, **kwargs):
        """
        Serializer for validating the parameters recieved to extract the data, it's important to notice
        that when the user requests to extract the data, the data it recieves on the post request is the
        same used on the query parameters to retrieve the data. This is used so we can build the file following 
        what the user have already defined. So sorts, filters and many other stuff are respected when retrieving the data.

        We also add `from_date` and `to_date` when retrieving the data, we use this so we can prevent the user from 
        retrieving all of the data of the formulary. And lastly we also add `format` required param that is the file format
        to extract the file.

        Args:
            user_id (int): what user is trying to retrieve the data
            company_id (int): from what company_id are you retrieving the data
            form_name (str): from what form_name you want to retrieve the data from
        """
        self.data_extract_service = DataExtractService(user_id=user_id, company_id=company_id, form_name=form_name)
        super(ExtractDataSerializer, self).__init__(**kwargs)
    # ------------------------------------------------------------------------------------------
    def validate(self, data):
        if self.data_extract_service.is_valid_data(data['from_date'], data['to_date'], 
                                              data.get('sort_value', []), data.get('sort_field', []),
                                              data.get('search_value', []), data.get('search_field', []), 
                                              data.get('search_exact', [])):
            return data
        else:
            raise serializers.ValidationError(detail='invalid_data')
    # ------------------------------------------------------------------------------------------
    def save(self):
        data = self.validated_data
        return self.data_extract_service.extract(data['format'], data['from_date'], data['to_date'], 
                                            data.get('sort_value', []), data.get('sort_field', []),
                                            data.get('search_value', []), data.get('search_field', []), 
                                            data.get('search_exact', []))

############################################################################################
class ExtractFormSerializer(serializers.ModelSerializer):
    depends_on_form = ExtractSectionRelation(many=True)
    # ------------------------------------------------------------------------------------------
    class Meta:
        model = Form
        fields = ('label_name', 'depends_on_form')

############################################################################################
class ExtractFileSerializer(serializers.Serializer):
    file_id = serializers.CharField()
    file = serializers.CharField()
    file_format = serializers.CharField()
    # ------------------------------------------------------------------------------------------
    def __init__(self, user_id, company_id, form_name, **kwargs):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name

        super(ExtractFileSerializer, self).__init__(**kwargs)
    # ------------------------------------------------------------------------------------------
    def create(self, validated_data):
        instance = ExtractFileData.objects.create(
            user_id=self.user_id, 
            company_id=self.company_id,
            form=Form.objects.filter(form_name=self.form_name).first(),
            file_id=validated_data['file_id'],
            file=validated_data['file'],
            file_format=validated_data['file_format']
        )
        return instance
    # ------------------------------------------------------------------------------------------
    class Meta:
        fields = ('file', 'file_format')