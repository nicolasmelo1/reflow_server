from rest_framework import serializers

from reflow_server.core.relations import ValueField
from reflow_server.formulary.relations import SectionRelation, FormRelation
from reflow_server.formulary.models import Form, Group
from reflow_server.authentication.models import UserExtended
from reflow_server.data.models import FormValue


class GetFormSerializer(serializers.ModelSerializer):
    """
    Retrives the data of a particular formulary with all of its fields, this data
    is used to build the formulary.

    Args:
        user_id (int): The id of the user for who you are trying to retrieve the form to
    """
    depends_on_form = SectionRelation(many=True)

    def __init__(self, user_id, **kwargs):
        kwargs['context'] = {
            'user_id': user_id
        }
        super(GetFormSerializer, self).__init__(**kwargs)

    class Meta:
        model = Form
        fields = ('id', 'form_name', 'group_id', 'label_name', 'depends_on_form')


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


class FormFieldTypeOptionsSerializer(serializers.ModelSerializer):
    value = ValueField(source='*')

    class Meta:
        model = FormValue
        fields = ('form_id', 'value')


class UserFieldTypeOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExtended
        fields = ('id', 'first_name', 'last_name')