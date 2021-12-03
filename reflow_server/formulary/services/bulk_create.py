from django.db import transaction

from reflow_server.formulary.models import SectionType
from reflow_server.formulary.services.data import FieldOptionsData
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.formulary.services.group import GroupService
from reflow_server.formulary.services.sections import SectionService
from reflow_server.formulary.services.fields import FieldService
from reflow_server.data.services.bulk_create import BulkCreateRecordsFormularyData, BulkCreateDataService

import uuid


class BulkCreateException(Exception):
    pass


class BulkCreateFieldData:
    def __init__(self, label_name, required, number_configuration_number_format_type, 
                 date_configuration_date_format_type, period_configuration_period_interval_type, 
                 field_type):
        self.label_name = label_name
        self.required = required
        self.number_configuration_number_format_type = number_configuration_number_format_type
        self.date_configuration_date_format_type = date_configuration_date_format_type
        self.period_configuration_period_interval_type = period_configuration_period_interval_type
        self.field_type = field_type
        self.field_options_data = None

    def add_field_option(self, option):
        if self.field_options_data == None:
            self.field_options_data = FieldOptionsData()

        return self.field_options_data.add_field_option(option)

class BulkCreateSectionData:
    def __init__(self, section_name):
        """
        Represents a new section that you wish to bulk create inside of reflow. This will hold all of the fields of this new section
        to bulk create inside of reflow.

        Args:
            section_name (str): The label_name of the section that you wish to create.
        """
        self.section_name = section_name
        self.fields = []

    def add_field(self, label_name, required, number_configuration_number_format_type, 
                  date_configuration_date_format_type, period_configuration_period_interval_type, field_type):
        """
        Adds a new field to the section.

        Args:
            label_name (str): The label_name of the field.
            required (bool): Whether or not the field is required.
            number_configuration_number_format_type (FieldNumberFormatType, None): The number_configuration_number_format_type of the field.
            date_configuration_date_format_type (FieldDateFormatType, None): The date_configuration_date_format_type of the field.
            period_configuration_period_interval_type (FieldPeriodIntervalType, None): The period_configuration_period_interval_type of the field.
            field_type (FieldType): The field_type of the field.
        
        Returns:
            BulkCreateFieldData: The newly created field.
        """
        field = BulkCreateFieldData(
            label_name, required, number_configuration_number_format_type, 
            date_configuration_date_format_type, period_configuration_period_interval_type, field_type
        )
        self.fields.append(field)
        return field

class BulkCreateFormularyData:
    def __init__(self, name):
        """
        Represents a new formulary inside of the group, this will have the formulary name with the sections and fields.

        Args:
            name (str): The label_name of the formulary.
        """
        self.name = name
        self.sections = []
        self.formulary_records_data = []

    def add_section(self, section_name):
        """
        Adds a new section to the formulary in the order that you want to create it.

        Args:
            section_name (str): The label_name of the section.
        """
        section = BulkCreateSectionData(section_name)
        self.sections.append(section)
        return section

    def add_formulary_records(self):
        """
        This is used so you can add the formulary records to the formulary, so after the formulary is created we 
        can add the formulary records to it without any issues. This is not obligatory but optional, you can just create
        the formularies if you want and the data separately.
        
        Returns:
            reflow_server.data.services.bulk_create.BulkCreateRecordsFormularyData: The newly created formulary records.
        """
        formulary_record_data = BulkCreateRecordsFormularyData(self.name)
        self.formulary_records_data.append(formulary_record_data)
        return formulary_record_data

class BulkCreateGroupData:
    def __init__(self, name):
        """
        Adds a new group to the bulk creation. When we bulk create something we will always
        append the formularies, sections and fields to a single group inside of the bulk creation.

        We do not create many groups when we bulk create formularies, fields and sections, right now
        there is no possible way to create more than one group in a single transaction.

        Args:
            name (str): The name of the group.
        """
        self.name = name
        self.formularies = []
    
    def add_formulary(self, name):
        """
        Appends a list of formularies to a single group.

        Args:
            name (str): The name of the formularies.
            section_name (str): The name of the only section inside of the formulary.
        """
        formulary = BulkCreateFormularyData(name)
        self.formularies.append(formulary)
        return formulary


class BulkCreateService:
    def __init__(self, user_id, company_id):
        """
        This is responsible for bulk creating the groups, formularies, sections and fields. This creates everything in one go 
        and in a single transaction. Because we need to create it in a single transaction we can't use each view individually as 
        we are used to.

        Args:
            user_id: The user id of the user who is creating the formularies
            company_id: The company id of the company who is creating the formularies
        """
        self.company_id = company_id
        self.user_id = user_id
        self.formularies = []
        self.formularies_records = []
    
    def add_bulk_create_data(self, group_name):
        """
        Creates a new BulkCreateGroupData object, this will hold the data needed to create a group, formularies, sections and fields
        in a single transaction. Instead of depending on the serializer format we define the format that we need here so it becomes
        a lot easier to have a default format for the data.

        Args:
            group_name (str): The name of the group.

        Returns:
            BulkCreateGroupData: The object that holds the data needed to create a group, formularies, sections and fields.
        """
        self.bulk_create_data = BulkCreateGroupData(group_name)
        return self.bulk_create_data

    @transaction.atomic
    def save(self):
        """
        Bulk create the formularies in a single transaction so if any error happens while creating the formulary the save
        process will not be affected.

        Args:
            group_name: The name of the group that the formularies will be created under
        
        Returns:
            reflow_server.formulary.models.Group: The group that the formularies were created
        """
        if hasattr(self, 'bulk_create_data'):
            group_service = GroupService(self.company_id)
            group = group_service.create_group(self.bulk_create_data.name)
            formulary_service = FormularyService(self.user_id, self.company_id)
            section_id_by_label_name = {}
            field_by_label_name = {}

            for formulary_index, formulary_data in enumerate(self.bulk_create_data.formularies):
                formulary = formulary_service.save_formulary(
                    enabled=True, 
                    label_name=formulary_data.name, 
                    order=formulary_index, 
                    group=group
                )

                section_type = SectionType.objects.filter(type='form').first()
                section_service = SectionService(self.user_id, self.company_id, formulary.id)
                field_service = FieldService(self.user_id, self.company_id, formulary.id)
                
                for section_index, section_data in enumerate(formulary_data.sections):
                    section = section_service.save_section(
                        enabled=True,
                        label_name=section_data.section_name, 
                        order=section_index, 
                        conditional_value=None,
                        section_type=section_type,
                        conditional_type=None,
                        conditional_on_field=None,
                        show_label_name=True,
                        conditional_excludes_data_if_not_set=True 
                    )
                    section_id_by_label_name[section_data.section_name] = section.id

                    for field_index, field_data in enumerate(section_data.fields):
                        field = field_service.save_field(
                            enabled=True,
                            label_name=field_data.label_name,
                            order=field_index,
                            is_unique=False,
                            field_is_hidden=False,
                            label_is_hidden=False,
                            placeholder='',
                            required=field_data.required,
                            section=section,
                            form_field_as_option=None,
                            formula_configuration=None,
                            is_long_text_a_rich_text=False,
                            date_configuration_auto_create=False,
                            date_configuration_auto_update=False,
                            number_configuration_number_format_type=field_data.number_configuration_number_format_type,
                            date_configuration_date_format_type=field_data.date_configuration_date_format_type,
                            period_configuration_period_interval_type=field_data.period_configuration_period_interval_type,
                            field_type=field_data.field_type,
                            field_options_data=field_data.field_options_data
                        )
                        field_by_label_name[field_data.label_name] = field

                # We will only create the data if the data was added to the formulary, otherwise we don't fill it as being obligatory.
                # remember that the data that we added as helper functions are not the data that we use to create the formulary records
                # for that we will use the reflow_server.data.services.formulary.FormularyDataService to create the formulary records
                if len(formulary_data.formulary_records_data) > 0:
                    bulk_create_data_service = BulkCreateDataService(self.company_id, self.user_id)
                    for bulk_create_formulary_record_data in formulary_data.formulary_records_data:
                        formulary_record_data = bulk_create_data_service.append_new_formulary(formulary.form_name)
                        
                        for bulk_create_section_record_data in bulk_create_formulary_record_data.sections:
                            section_record_data = formulary_record_data.add_section_data(
                                section_id=section_id_by_label_name[bulk_create_section_record_data.label_name], 
                                uuid=str(uuid.uuid4()) 
                            )

                            for bulk_create_field_record_data in bulk_create_section_record_data.fields:
                                section_record_data.add_field_value(
                                    field_id = field_by_label_name[bulk_create_field_record_data.label_name].id,
                                    field_name = field_by_label_name[bulk_create_field_record_data.label_name].name,
                                    value = bulk_create_field_record_data.value
                                )
                    
                    self.formularies_records.append(bulk_create_data_service)

            return group
        else:
            raise BulkCreateException('You need to call `.add_bulk_create_data()` method to add your formularies and field data before calling ' 
                                      '`.{}()`'.format(__name__))

    @transaction.atomic
    def save_formularies_records(self):
        """
        Save the formularies records that were created in the `.save()` method.
        """
        if hasattr(self, 'formularies_records'):
            for bulk_create_data_service in self.formularies_records:
                bulk_create_data_service.save(is_async=True)
        else:
            raise BulkCreateException('You need to call `.add_bulk_create_data()` method to add your formularies and field data before calling ' 
                                    '`.{}()`'.format(__name__))