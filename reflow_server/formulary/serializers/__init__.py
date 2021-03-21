from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.formulary.relations import SectionRelation, FormRelation, PublicAccessFieldRelation
from reflow_server.formulary.models import Form, Group, PublicAccessForm
from reflow_server.formulary.services.public import PublicFormularyService
from reflow_server.authentication.models import UserExtended
from reflow_server.data.models import FormValue


############################################################################################
class GetFormSerializer(serializers.ModelSerializer):
    """
    Retrives the data of a particular formulary with all of its fields, this data
    is used to build the formulary.

    Context Args:
        user_id (int): The id of the user for who you are trying to retrieve the form to
        public_access_key(str): The public access key used by unauthenticated users
    """
    depends_on_form = SectionRelation(many=True)

    class Meta:
        model = Form
        fields = ('id', 'form_name', 'group_id', 'label_name', 'depends_on_form')


############################################################################################
class GetGroupSerializer(serializers.ModelSerializer):
    """
    Retrieve groups with the forms for a particular user.

    Context Args:
        user_id (int): The id of the user for who you are trying to retrieve all forms
    """
    form_group = FormRelation(many=True)
    
    class Meta:
        model = Group
        fields = ('id', 'form_group','name')


############################################################################################
class FormFieldTypeOptionsSerializer(serializers.ModelSerializer):
    value = ValueField(source='*')

    class Meta:
        model = FormValue
        fields = ('form_id', 'value')


############################################################################################
class UserFieldTypeOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = ('id', 'first_name', 'last_name')


############################################################################################
class PublicAccessFormSerializer(serializers.ModelSerializer):
    greetings_message = serializers.CharField(allow_blank=True, allow_null=True)
    description_message = serializers.CharField(allow_blank=True, allow_null=True)
    is_to_submit_another_response_button = serializers.BooleanField(default=False)
    form_label_name = serializers.CharField(source='form.label_name', required=False)
    public_access_key = serializers.CharField(source='public_access.public_key', required=False)
    public_access_form_public_access_fields = PublicAccessFieldRelation(many=True)

    def save(self, form_id, company_id, user_id):
        field_ids = [public_access_field['field_id'] for public_access_field in self.validated_data.get('public_access_form_public_access_fields', [])]
        return PublicFormularyService.update_public_formulary(
            company_id, 
            user_id, 
            form_id, 
            field_ids,
            self.validated_data.get('greetings_message', None),
            self.validated_data.get('description_message', None),
            self.validated_data.get('is_to_submit_another_response_button')
        )

    class Meta:
        model = PublicAccessForm
        fields =('form_id', 'description_message', 'greetings_message', 'is_to_submit_another_response_button', 'public_access_key', 'form_label_name', 'public_access_form_public_access_fields')
