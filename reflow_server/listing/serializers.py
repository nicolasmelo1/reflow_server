from rest_framework import serializers

from reflow_server.data.models import DynamicForm
from reflow_server.formulary.models import Form
from reflow_server.listing.services.extract import ExtractService
from reflow_server.listing.models import ListingSelectedFields, ExtractFileData
from reflow_server.listing.relations import ListingHeaderFieldsRelation, ExtractFormValueRelation, ExtractSectionRelation


class ListingHeaderSerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving the headers of listing visualization.
    """
    id = serializers.IntegerField(required=False, allow_null=True)
    field = ListingHeaderFieldsRelation()

    def create(self, validated_data):
        instance, created = ListingSelectedFields.objects.update_or_create(
            id=validated_data.get('id', None),
            defaults={
                'field_id': validated_data['field']['id'],
                'is_selected': validated_data['is_selected'],
                'user_id': self.context['user_id']
            }
        )
        return instance
        
    class Meta:
        model = ListingSelectedFields
        fields = ('id', 'field', 'is_selected')


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
        self.extract_service = ExtractService(user_id=user_id, company_id=company_id, form_name=form_name)
        super(ExtractDataSerializer, self).__init__(**kwargs)

    def validate(self, data):
        if self.extract_service.is_valid_data(data['from_date'], data['to_date'], 
                                              data.get('sort_value', []), data.get('sort_field', []),
                                              data.get('search_value', []), data.get('search_field', []), 
                                              data.get('search_exact', [])):
            return data
        else:
            raise serializers.ValidationError(detail='invalid_data')
    
    def save(self):
        data = self.validated_data
        self.extract_service.extract(data['format'], data['from_date'], data['to_date'], 
                                     data.get('sort_value', []), data.get('sort_field', []),
                                     data.get('search_value', []), data.get('search_field', []), 
                                     data.get('search_exact', []))


class ExtractFormDataSerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving the data of a user to the reflow_worker application
    to build csv file data to extract.

    Context Args:
        fields (list(str)): List of string names to add to your data
        company_id (int): Id of the company that you are trying to extract the data to
    """
    dynamic_form_value = ExtractFormValueRelation(many=True)
    
    class Meta:
        model = DynamicForm
        fields = ('id', 'user', 'dynamic_form_value')


class ExtractFormSerializer(serializers.ModelSerializer):
    depends_on_form = ExtractSectionRelation(many=True)

    class Meta:
        model = Form
        fields = ('id', 'form_name', 'group_id', 'label_name', 'depends_on_form')


class ExtractFileSerializer(serializers.Serializer):
    file = serializers.CharField()
    file_format = serializers.CharField()

    def __init__(self, user_id, company_id, form_name, **kwargs):
        self.user_id = user_id
        self.company_id = company_id
        self.form_name = form_name

        super(ExtractFileSerializer, self).__init__(**kwargs)

    def create(self, validated_data):
        instance = ExtractFileData.objects.create(
            user_id=self.user_id, 
            company_id=self.company_id,
            form=Form.objects.filter(form_name=self.form_name).first(),
            file=validated_data['file'],
            file_format=validated_data['file_format']
        )
        return instance
    
    class Meta:
        fields = ('file', 'file_format')