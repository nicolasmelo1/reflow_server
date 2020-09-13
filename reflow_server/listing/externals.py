from django.conf import settings

from reflow_server.core import externals
from reflow_server.data.models import DynamicForm
from reflow_server.formulary.models import Form
from reflow_server.listing.serializers import ExtractFormDataSerializer, ExtractFormSerializer


class ExtractDataWorkerExternal(externals.External):
    host = settings.EXTERNAL_APPS['reflow_worker'][0]

    def build_extraction_data(self, file_id, file_format, company_id, user_id, form_id, field_ids, dynamic_form_ids):
        """
        Sends the data needed for the REFLOW_WORKER app to create the files. The reflow_worker creates the file
        as a csv and sends it back as a base64 string so we convert to the user desired format here when downloading

        Args:
            file_id (str): A unique id of the file, this way even if the user tries to extract multiple files we grant that
                           the user will extract the exact file_id he wants
            file_format (('.csv', '.xlsx')): Right now only '.csv' and '.xlsx' file formats are supported
            company_id (int): The id of a reflow_server.authentication.models.Company instance
            user_id (int): The id of a reflow_server.authentication.models.UserExtended instance
            form_id (int): The id of a reflow_server.formulary.models.Form instance, this is the MAIN form, 
                           so the ones with depends_on as None, it is not a section.
            field_ids (list(int)): The ids of many reflow_server.formulary.models.Field instances, this is used
                                   so we can filter the columns of the file, usually it's the one he has 
                                   selected on the listing.
            dynamic_form_ids (list(int)): The ids of many reflow_server.data.models.DynamicForm instances, this
                                          is the ids of the formulary data you want to retrive on the file. 
                                          Basically, each row.

        Returns:
            request.Response: The response of the POST request.
        """
        dynamic_forms = DynamicForm.listing_.dynamic_forms_by_dynamic_form_ids_ordered(dynamic_form_ids)
        form = Form.objects.filter(id=form_id).first()
        url = '/data/external/extraction/{company_id}/{user_id}/{form_name}/'.format(
            company_id=company_id,
            user_id=user_id, 
            form_name=form.form_name
        )
        
        form_serializer = ExtractFormSerializer(instance=form)
        form_data_serializer = ExtractFormDataSerializer(instance=dynamic_forms, many=True, context={
            'company_id': company_id, 
            'fields': field_ids
        })
        return self.post(url, data={
            'file_id': file_id,
            'params': {
                'fields': field_ids
            },
            'format': file_format,
            'form': form_serializer.data,
            'data': form_data_serializer.data
        })