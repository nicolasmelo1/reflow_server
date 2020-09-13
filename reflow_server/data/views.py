from django.shortcuts import redirect
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.utils.storage import Bucket, BucketUploadException
from reflow_server.core.utils.pagination import Pagination
from reflow_server.data.serializers import FormDataSerializer, DataSerializer
from reflow_server.data.models import DynamicForm, Attachments
from reflow_server.data.services.data import DataService
from reflow_server.formulary.models import Form

import urllib
import json
import math


class DataView(APIView):
    """
    This view is used for retrieving data for visualization types like kanban or listing.
    It's important to understand that this returns a list of items to this visualization types also the data
    is formatted.

    Methods:
        .get() -- Retrieves a list of formularies data from a single form.
    """
    def __extact_fields_from_request_query_params(self, query_params):
        if 'fields' in query_params:
            fields_query_param = query_params.getlist('fields', list())
        else:
            fields_query_param = query_params.getlist('fields[]', list())
        return fields_query_param

    def get(self, request, company_id, form):
        pagination = Pagination.handle_pagination(
            current_page=int(request.query_params.get('page', 1)),
            items_per_page=15
        )        

        fields = self.__extact_fields_from_request_query_params(request.query_params)

        form_id = Form.objects.filter(group__company_id=company_id, form_name=form).first().id
        form_data_accessed_by_user = DataService.get_user_form_data_ids_from_query_params(
            query_params=request.query_params, 
            user_id=request.user.id,
            company_id=company_id,
            form_id=form_id
        )
        
        instances = DynamicForm.data_.dynamic_forms_by_dynamic_form_ids_ordered(form_data_accessed_by_user)[pagination.offset:pagination.limit]
        serializer = DataSerializer(instance=instances, many=True, context={
            'fields': fields,
            'company_id': company_id
        })
        
        return Response({
            'status': 'ok',
            'pagination': {
                'current': pagination.current_page,
                'total': pagination.get_total_number_of_pages(len(form_data_accessed_by_user))
            },
            'data': serializer.data
        })


@method_decorator(csrf_exempt, name='dispatch')
class FormularyDataView(APIView):
    """
    View used for saving a new formulary data.

    Methods:
        .post() -- saves a new data to a specific form_name
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def post(self, request, company_id, form):
        files = {key:request.data.getlist(key) for key in request.data.keys() if key != 'data'}
        serializer = FormDataSerializer(user_id=request.user.id, company_id=company_id, form_name=form, data=json.loads(request.data.get('data', '\{\}')))
        if serializer.is_valid():
            try:
                serializer.save(files=files)
                return Response({
                    'status': 'ok'
                }, status=status.HTTP_200_OK)

            except BucketUploadException as bue:
                return Response({
                    'status': 'error',
                    'error': json.loads(str(bue))
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    

class FormularyDataEditView(APIView):
    """
    View used for editing the data of a formulary data. So if you are trying to
    edit the data of a formulary, use this view. 

    Methods:
        .get() -- gets the data of a form_data_id
        .post() -- updates a specific form_data_id with new data to a specific form_name
        .delete() -- deletes the data of a form_data_id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, company_id, form, dynamic_form_id):
        instance = DynamicForm.data_.dynamic_form_by_dynamic_form_id_and_company_id(
            dynamic_form_id,
            company_id,
            form
        )

        serializer = FormDataSerializer(
            instance=instance.depends_on if instance.depends_on else instance,
            user_id=request.user.id, 
            company_id=company_id, 
            form_name=form
        )
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, company_id, form, dynamic_form_id):
        duplicate = 'duplicate' in request.query_params
        files = {key:request.data.getlist(key) for key in request.data.keys() if key != 'data'}
        serializer = FormDataSerializer(
            user_id=request.user.id, 
            company_id=company_id, 
            form_name=form,
            form_data_id=dynamic_form_id,
            duplicate=duplicate,
            data=json.loads(request.data.get('data', '\{\}'))
        )
        if serializer.is_valid():
            try:
                serializer.save(files=files)
                return Response({
                    'status': 'ok'
                }, status=status.HTTP_200_OK)

            except BucketUploadException as bue:
                return Response({
                    'status': 'error',
                    'error': json.loads(str(bue))
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, form, dynamic_form_id):
        DynamicForm.data_.remove_dynamic_form_by_dynamic_form_id_company_id_and_form_name(
            dynamic_form_id,
            company_id,
            form
        )
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)



class DownloadFileView(APIView):
    """
    Redirects the user for a new generated and timed url so the user can download the file in his desktop or phone.
    The file is protected in s3 so normal users cannot access it, when a user wants to download this view is responsible
    for generating a new temporary url so he can download the file.

    Methods:
        .get() -- This is not a normal API view since it makes a redirection, be aware of that, it's better if you call this
                  in a new tab for the user.
    """
    def get(self, request, company_id, form, dynamic_form_id, field_id, file_name):
        attachment = Attachments.data_.attachment_by_dynamic_form_id_field_id_and_file_name(dynamic_form_id, field_id, file_name)
        if attachment:
            if attachment.file_url and len(attachment.file_url.split('/{}/'.format(attachment.file_attachments_path)))>1:
                key = attachment.file_attachments_path + '/' + attachment.file_url.split('/{}/'.format(attachment.file_attachments_path))[1]
                key = urllib.parse.unquote(key)
            else:
                key = '{file_attachments_path}/{id}/{field}/{file_name}'.format(
                    id=attachment.form_id, field=attachment.field_id,
                    file_attachments_path=attachment.file_attachments_path,
                    file_name=attachment.file
                )
            bucket = Bucket(settings.S3_BUCKET)
            url = bucket.get_temp_url(key)
            return redirect(url)
            