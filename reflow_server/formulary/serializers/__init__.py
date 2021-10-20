from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.data.services.representation import RepresentationService
from reflow_server.formulary.relations import SectionRelation, FormRelation, PublicAccessFieldRelation
from reflow_server.formulary.models import Form, Group, PublicAccessForm
from reflow_server.formulary.services.public import PublicFormularyService
from reflow_server.authentication.models import UserExtended
from reflow_server.data.models import DynamicForm, FormValue

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
    """
    Yes, this is strange, but since we match to the formulary and not section we need to do this in order to display all the 
    options formated.

    But why formated? Because sometimes we can match for more than one formValue (the value is from a multi_section) so we display
    the value to the user like "value1 | value2"
    """
    def to_representation(self, instance):
        form_values = FormValue.objects.filter(field_id=self.context['field_id'], form__depends_on=instance)
        represented_values = []
        for form_value in form_values:
            representation_service = RepresentationService(
                form_value.field_type,
                form_value.date_configuration_date_format_type_id,
                form_value.number_configuration_number_format_type_id,
                form_value.form_field_as_option_id
            )
            represented_values.append(representation_service.representation(form_value.value))
        return {
            'value': ' | '.join(represented_values),
            'form_id': instance.id,
            'uuid': instance.uuid
        }

    class Meta:
        model = DynamicForm
        fields = '__all__'
############################################################################################
class UserFieldTypeOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = ('id', 'first_name', 'last_name', 'email')


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
