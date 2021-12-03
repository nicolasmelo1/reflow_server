from django.db import transaction

from reflow_server.data.services.formulary import FormularyDataService
from reflow_server.core.utils.asynchronous import RunAsyncFunction

import uuid


class BulkCreateRecordsFieldData:
    def __init__(self, field_label_name, value):
        self.label_name = field_label_name
        self.value = value


class BulkCreateRecordsSectionData:
    def __init__(self, section_label_name):
        self.label_name = section_label_name
        self.values_by_field_label_name = {}
        self.fields = []

    def add_field(self, field_label_name, value):
        self.values_by_field_label_name[field_label_name] = self.values_by_field_label_name.get(field_label_name, []) + \
            [value]
        self.fields.append(BulkCreateRecordsFieldData(field_label_name, value))


class BulkCreateRecordsFormularyData: 
    def __init__(self, formulary_label_name):
        """
        This is a helper class that will be used when needed to translate the data recieved from the client into a python
        format. This way we then can append the data with `.append_new_formulary()` easily.
        """
        self.formulary_label_name = formulary_label_name
        self.sections_by_label_name = {}
        self.sections = []

    def add_section(self, section_label_name):
        bulk_create_records_section_data = BulkCreateRecordsSectionData(section_label_name)
        self.sections_by_label_name[section_label_name] = self.sections_by_label_name.get(section_label_name, []) + \
            [bulk_create_records_section_data]
        self.sections.append(bulk_create_records_section_data)
        return bulk_create_records_section_data


class BulkCreateDataService:
    def __init__(self, company_id, user_id):
        """
        Service used for bulk creating records inside of formularies inside of reflow. We don't do any distinction between the formularies that we are bulk creating data
        we can create records in 3 different formularies for example one after another repeated n times. We just need the data to save the records to.

        Args:
            company_id (int): The id of the company that we are bulk creating data for.
            user_id (int): The id of the user that we are bulk creating data for.
        """
        self.company_id = company_id
        self.user_id = user_id
        self.formulary_records = []

    def append_new_formulary(self, formulary_name):
        """
        We add data in reflow by using the FormularyDataService, this will respect the formatting of the numbers, dates, run formulas and so on.
        This means that every record you want to create MUST use this service. In other words, since this is for bulk creating records, each record is
        represented as an instance of this class.

        Then we append the instance of this class inside of `formulary_records` list, so we can loop it after to save all of the data.

        Args:
            formulary_name (str): The name of the formulary to create the records in. This is the form_name and NOT the label_name.

        Returns:
            reflow_server.data.services.formulary.data.FormularyData: An instance of the FormularyData class. This will be used to add the sections data and 
                                                                      fields data to the formulary
        """
        formulary_data_service = FormularyDataService(self.user_id, self.company_id, formulary_name, disable_events=True)
        formulary_data = formulary_data_service.add_formulary_data(str(uuid.uuid4()))
        self.formulary_records.append(formulary_data_service)
        return formulary_data

    def save(self, is_async=False):
        """
        We save all of the data in a single transaction, it's important to note that since data can be toooooo large, we need a way
        to save it asyncronously as other operations happen inside of reflow. If we didn't do this, then saving the data would take too long.

        Args:
            is_async (bool): If we want to save the data asyncronously, in parallel of other things inside of reflow, set this to true.
                             usually save asyncronously is best for bulk creating data, but you can also save in sync if you want.
        """
        @transaction.atomic
        def save_formulary_data():
            for formulary_data_service in self.formulary_records:
                is_formulary_data_valid = formulary_data_service.is_valid()
                if is_formulary_data_valid:
                    formulary_data_service.save()
        if is_async:
            async_task = RunAsyncFunction(save_formulary_data)
            async_task.delay()
        else:
            save_formulary_data()
    
