from django.db import transaction

from rest_framework import serializers

from reflow_server.formulary.models import FormulaVariable, Group, Form, Field, FieldOptions, DefaultFieldValue
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.group import GroupService
from reflow_server.formulary.services.sections import SectionService
from reflow_server.formulary.services.fields import FieldService
from reflow_server.formulary.services.bulk_create import BulkCreateService
from reflow_server.formulary.services.data import FieldOptionsData, DefaultFieldData, FormulaVariableData
from reflow_server.formulary.relations import DefaultFieldValueValue


############################################################################################
class FieldOptionsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    label_name = serializers.CharField()
    form_id = serializers.IntegerField(source='form.depends_on_id')
    form_label_name = serializers.CharField(source='form.depends_on.label_name')
    group_id = serializers.IntegerField(source='form.depends_on.group_id')
    group_name = serializers.CharField(source='form.depends_on.group.name')

    class Meta:
        model = Field
        fields = ('id', 'label_name', 'form_id', 'form_label_name', 'group_id', 'group_name')


############################################################################################
class FieldFormulaVariablesSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField()
    variable_id = serializers.IntegerField()

    class Meta:
        model = FormulaVariable
        fields = ('uuid', 'variable_id')


############################################################################################
class FieldDefaultValuesSerializer(serializers.ModelSerializer):
    value = DefaultFieldValueValue(source='*')
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = DefaultFieldValue
        fields = ('id', 'value')

############################################################################################
class FieldOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)
    
    class Meta:
        model = FieldOptions
        fields = ('id', 'uuid', 'option',)

############################################################################################
class FieldSerializer(serializers.ModelSerializer):
    """
    Serializer for editing fields and to be used when loading as the child of a section.

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
        form_id (int): the form_id for which form does this field references to (it is the MAIN FORM not section_id).
    """
    id = serializers.IntegerField(allow_null=True)
    field_option = FieldOptionSerializer(many=True)
    field_formula_variables = FieldFormulaVariablesSerializer(many=True)
    field_default_field_values = FieldDefaultValuesSerializer(many=True)
    name = serializers.CharField(allow_blank=True, allow_null=True)
    order = serializers.IntegerField(allow_null=True, required=False, default=1)

    def validate_form_field_as_option(self, value):
        if hasattr(self, 'initial_data') and 'type' in self.initial_data and self.initial_data['type'] and value != None:
            is_form_field_type_not_valid = FieldService.is_form_field_type_not_valid(
                field_type_id=self.initial_data['type'],
                form_field_as_option_field_id=value
            )
            if is_form_field_type_not_valid:
                raise serializers.ValidationError(detail={'detail': 'form fields must have a connection', 'reason': 'form_fields_connection'})
        return value

    def validate_field_option(self, value): 
        if hasattr(self, 'initial_data') and 'type' in self.initial_data and self.initial_data['type'] and value != None:
            is_option_field_type_not_valid = FieldService.is_option_field_type_not_valid(
                field_type_id=self.initial_data['type'],
                field_options_length=len(value)
            )
            if is_option_field_type_not_valid:
                raise serializers.ValidationError(detail={'detail': 'option field must have a option', 'reason': 'option_field_empty_option'})
        return value

    def validate_label_name(self, value):
        if hasattr(self, 'initial_data') and 'type' in self.initial_data and self.initial_data['type']:
            has_field_with_label_name = FieldService.is_label_name_not_unique(
                field_id=self.initial_data.get('id', None),
                company_id=self.context['company_id'],
                section_id=self.initial_data.get('form', None),
                label_name=value
            )
            if has_field_with_label_name:
                raise serializers.ValidationError(detail={'detail': 'label names should be unique', 'reason': 'label_name_already_exists'})
        return value

    @transaction.atomic
    def save(self):
        if self.instance:
            instance = self.instance
        else:
            instance = self.Meta.model()

        if self.validated_data['form_field_as_option'] != None:
            form_field_as_option = Field.formulary_.field_by_field_id_main_form_id_and_company_id(
                field_id=self.validated_data['form_field_as_option'].id,
                company_id=self.context['company_id']
            )
        else:
            form_field_as_option = None
        
        field_options_data = FieldOptionsData()
        formula_configuration = self.validated_data['formula_configuration'] if self.validated_data.get('formula_configuration', None) not in [None, ''] else None 
        for field_option in self.validated_data.get('field_option', list()):
            field_options_data.add_field_option(field_option['option'], field_option['uuid'], field_option['id'])

        default_field_value_data = list()
        for default_field_value in self.validated_data.get('field_default_field_values', list()):
            default_field_value_data.append(
                DefaultFieldData(
                    default_value_id=default_field_value.get('id'), 
                    value=default_field_value.get('value')
                )
            )

        field_formula_variables = list()
        for field_formula_variable in self.validated_data.get('field_formula_variables', list()):
            if field_formula_variable.get('variable_id', None):
                field_formula_variables.append(
                    FormulaVariableData(
                        variable_id=field_formula_variable.get('variable_id'),
                        variable_uuid=field_formula_variable.get('uuid')
                    )
                )
        
        field_service = FieldService(
            user_id=self.context['user_id'], 
            company_id=self.context['company_id'], 
            form_id=self.context['form_id']
        )
        
        instance = field_service.save_field(
            enabled=self.validated_data['enabled'],
            label_name=self.validated_data['label_name'],
            order=self.validated_data['order'],
            is_unique=self.validated_data['is_unique'],
            field_is_hidden=self.validated_data['field_is_hidden'],
            label_is_hidden=self.validated_data['label_is_hidden'],
            placeholder=self.validated_data.get('placeholder', None),
            required=self.validated_data['required'],
            section=self.validated_data['form'],
            form_field_as_option=form_field_as_option,
            formula_configuration=formula_configuration,
            is_long_text_a_rich_text=self.validated_data['is_long_text_rich_text'],
            date_configuration_auto_create=self.validated_data['date_configuration_auto_create'],
            date_configuration_auto_update=self.validated_data['date_configuration_auto_update'],
            number_configuration_number_format_type=self.validated_data.get('number_configuration_number_format_type', None),
            date_configuration_date_format_type=self.validated_data.get('date_configuration_date_format_type', None),
            period_configuration_period_interval_type=self.validated_data.get('period_configuration_period_interval_type', None),
            field_type=self.validated_data['type'],
            field_uuid=self.validated_data['uuid'],
            default_field_value_data=default_field_value_data,
            field_formula_variables=field_formula_variables,
            field_options_data=field_options_data,
            instance=instance
        )
        return instance

    class Meta:
        model = Field
        exclude = ('created_at', 'updated_at')


############################################################################################
class SectionSerializer(serializers.ModelSerializer):
    """
    Serializer for editing sections and to be used when loading as the child of a formulary.

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
        form_id (int): the form_id for which form does this section references to.
    """
    id = serializers.IntegerField(allow_null=True)
    form_name = serializers.CharField(allow_blank=True, allow_null=True)
    form_fields = FieldSerializer(many=True, required=False, allow_null=True)

    def validate(self, data):
        self.section_service = SectionService(
            user_id=self.context['user_id'], 
            company_id=self.context['company_id'], 
            form_id=self.context['form_id']
        )
        if self.section_service.check_if_unique_section_label_name(data['label_name'], self.instance.id if self.instance else None):
            raise serializers.ValidationError(detail={'detail': 'label_name', 'reason': 'must_be_unique'})
        else:
            return data

    def save(self):
        if self.instance:
            instance = self.instance
        else:
            instance = self.Meta.model()

        instance = self.section_service.save_section(
            enabled=self.validated_data['enabled'],
            label_name=self.validated_data['label_name'],
            order=self.validated_data['order'],
            show_label_name=self.validated_data['show_label_name'],
            conditional_excludes_data_if_not_set=self.validated_data['conditional_excludes_data_if_not_set'],
            conditional_value=self.validated_data['conditional_value'] if self.validated_data.get('conditional_value', None) and self.validated_data['conditional_value'] != '' else None,
            section_type=self.validated_data['type'],
            section_uuid=self.validated_data['uuid'],
            conditional_type=self.validated_data.get('conditional_type', None),
            conditional_on_field=self.validated_data.get('conditional_on_field', None),
            instance=instance
        )
        return instance

    class Meta:
        model = Form
        exclude = ('company', 'depends_on', 'created_at', 'updated_at')


############################################################################################
class FormularyListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        formulary_service = FormularyService(user_id=self.context['user_id'], company_id=self.context['company_id'])
        forms = data.filter(id__in=formulary_service.formulary_ids_the_user_has_access_to, depends_on__isnull=True).order_by('order')
        return super(FormularyListSerializer, self).to_representation(forms)

class FormularySerializer(serializers.ModelSerializer):
    """
    Serializer for editing formularies and for loading to be used when loading groups formularies

    Args:
        is_loading_sections (bool, optional): Set this to true if you want to load the sections when you load the serializer. 
                                              Defaults to False.

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
    """
    id = serializers.IntegerField(allow_null=True)
    form_name = serializers.CharField(allow_null=True, allow_blank=True)
    depends_on_form = SectionSerializer(many=True, required=False, allow_null=True)

    def __init__(self, is_loading_sections=False, *args, **kwargs):
        super(FormularySerializer, self).__init__(*args, **kwargs)
        if not is_loading_sections:
            self.fields.pop('depends_on_form')

    def validate(self, data):
        self.formulary_service = FormularyService(user_id=self.context['user_id'], company_id=self.context['company_id'])
        if self.formulary_service.check_if_unique_formulary_label_name(data['label_name'], data['group'], data['id']):
            raise serializers.ValidationError(detail={'detail': 'label_name', 'reason': 'must_be_unique'})
        else:
            return data

    def save(self):
        if self.instance:
            instance = self.instance
        else:
            instance = self.Meta.model()

        instance = self.formulary_service.save_formulary(
            enabled=self.validated_data['enabled'], 
            label_name=self.validated_data['label_name'], 
            order=self.validated_data['order'], 
            group=self.validated_data['group'],
            instance=instance
        )
        return instance
    
    class Meta:
        model = Form
        list_serializer_class = FormularyListSerializer
        fields = ('id', 'label_name', 'form_name', 'enabled', 'group', 'order', 'depends_on_form')

############################################################################################
class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for editing groups and for loading to be used when loading groups

    Context Args:
        user_id (int): the user_id of who is editing the data
        company_id (int): for what company you are editing the data
    """
    id = serializers.IntegerField(allow_null=True)
    form_group = FormularySerializer(many=True, required=False, allow_null=True)

    def validate(self, data):
        self.group_service = GroupService(self.context['company_id'])
        if self.group_service.check_if_name_exists(data['name'], self.instance.id):
            raise serializers.ValidationError(detail={'detail': 'label_name', 'reason': 'must_be_unique'})
        else:
            return data

    def update(self, instance, validated_data):
        instance = self.group_service.update_group(
            instance, 
            validated_data['name'],
            validated_data['enabled'],
            validated_data['order']
        )
        return instance

    class Meta:
        model = Group
        fields = ('id', 'name', 'enabled', 'order', 'form_group')

############################################################################################
class BulkCreateFieldSerializer(serializers.ModelSerializer):
    field_option = FieldOptionSerializer(many=True)

    class Meta:
        model = Field
        fields = ['label_name',  'required', 'number_configuration_number_format_type', 
                  'date_configuration_date_format_type', 'period_configuration_period_interval_type',
                  'type', 'field_option']


class BulkCreateFieldRecordDataSerializer(serializers.Serializer):
    field_name = serializers.CharField()
    value = serializers.CharField(allow_blank=True)


class BulkCreateFormularyRecordDataSerializer(serializers.Serializer):
    """
    Serializer for bulk creating the formulary records. This is a list, each item in the list represent one of the fields inside 
    of the formulary.
    """
    data_by_each_field = BulkCreateFieldRecordDataSerializer(many=True)
    

class BulkCreateFormularySerializer(serializers.Serializer):
    """
    Relation used in the BulkCreateGroupSerializer to represent each formulary in reflow.
    """
    name = serializers.CharField()
    section_name = serializers.CharField()
    fields = BulkCreateFieldSerializer(many=True, required=True, allow_null=False)
    data = BulkCreateFormularyRecordDataSerializer(many=True, required=False, allow_null=True)

class BulkCreateGroupSerializer(serializers.Serializer):
    """
    Serializer that represents a Group of formularies that will be created in the bulk create process.

    Contexts:
        company_id (int): the company_id of the company that the group will be created for
        user_id (int): the user_id of the user that is creating the group
    """
    name = serializers.CharField()
    formularies = BulkCreateFormularySerializer(many=True, required=True, allow_null=False)

    def create(self, validated_data):
        bulk_create_service = BulkCreateService(self.context['user_id'], self.context['company_id'])
        group_data = bulk_create_service.add_bulk_create_data(validated_data['name'])
        for formulary in validated_data['formularies']:
            formulary_data = group_data.add_formulary(formulary['name'])
            section_data = formulary_data.add_section(formulary['section_name'])
            for field in formulary['fields']:
                field_data = section_data.add_field(
                    label_name=field['label_name'],
                    required=field.get('required', False),
                    number_configuration_number_format_type=field.get('number_configuration_number_format_type', None),
                    date_configuration_date_format_type=field.get('date_configuration_date_format_type', None), 
                    period_configuration_period_interval_type=field.get('period_configuration_period_interval_type', None), 
                    field_type=field['type']
                )
                for field_option in field['field_option']:
                    field_data.add_field_option(field_option['option'])
            if formulary.get('data', None):
                for data in formulary['data']:
                    formulary_records_data = formulary_data.add_formulary_records()
                    section_records_data = formulary_records_data.add_section(formulary['section_name'])
                    for field_data in data['data_by_each_field']:
                        section_records_data.add_field(field_data['field_name'], field_data['value'])
                                 
        result = bulk_create_service.save()
        bulk_create_service.save_formularies_records()
        return result