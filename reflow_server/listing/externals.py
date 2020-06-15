from django.conf import settings

from reflow_server.core import externals
from reflow_server.data.models import DynamicForm
from reflow_server.formulary.models import Form
from reflow_server.listing.serializers import ExtractFormDataSerializer, ExtractFormSerializer


class ExtractDataWorkerExternal(externals.External):
    host = settings.EXTERNAL_APPS['reflow_worker'][0]

    def build_extraction_data(self, file_format, company_id, user_id, form_id, field_ids, dynamic_form_ids):
        dynamic_forms = DynamicForm.objects.filter(id__in=dynamic_form_ids)
        form = Form.objects.filter(id=form_id).first()

        url = '/utils/extraction/{company_id}/{user_id}/{form_name}/'.format(
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
            'params': {
                'fields': field_ids
            },
            'format': file_format,
            'form': form_serializer.data,
            'data': form_data_serializer.data
        })