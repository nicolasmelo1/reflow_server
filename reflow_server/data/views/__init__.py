from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from reflow_server.authentication import serializers

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.utils.storage import BucketUploadException
from reflow_server.core.utils.pagination import Pagination
from reflow_server.data.serializers import FormDataSerializer, DataSerializer, LastValuesSerializer
from reflow_server.data.models import DynamicForm
from reflow_server.data.services import DataService, AttachmentService
from reflow_server.formulary.models import Form

import json


class DataView(APIView):
    """
    This view is used for retrieving data for visualization types like kanban or listing.
    It's important to understand that this returns a list of items to this visualization types also the data
    is formatted.

    Methods:
        GET: Retrieves a list of formularies data from a single form.
    """
    def __extact_fields_from_request_query_params(self, query_params):
        if 'fields' in query_params:
            fields_query_param = query_params.getlist('fields', list())
        else:
            fields_query_param = query_params.getlist('fields[]', list())
        return fields_query_param

    def get(self, request, company_id, form):
        formulary_instance = Form.objects.filter(group__company_id=company_id, form_name=form).first()

        if formulary_instance:
            pagination = Pagination.handle_pagination(
                current_page=int(request.query_params.get('page', 1)),
                items_per_page=15
            )        

            fields = self.__extact_fields_from_request_query_params(request.query_params)

            form_id = formulary_instance.id
            form_data_accessed_by_user = DataService.get_user_form_data_ids_from_query_params(
                query_params=request.query_params, 
                user_id=request.user.id,
                company_id=company_id,
                form_id=form_id
            )

            total_number_of_pages, main_form_data_ids_paginated = pagination.paginate_list(form_data_accessed_by_user)
            
            serializer_data = DataSerializer.retrieve_data(main_form_data_ids_paginated, company_id, fields)
            serializer = DataSerializer(data=serializer_data, many=True)
            data = serializer.initial_data
    
            return Response({
                'status': 'ok',
                'pagination': {
                    'current': pagination.current_page,
                    'total': total_number_of_pages
                },
                'data': data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'reason': 'form_name_does_not_exist'
            }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class FormularyDataView(APIView):
    """
    View used for saving a new formulary data.

    Methods:
        POST: saves a new data to a specific form_name
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, form):
        serializer = FormDataSerializer(
            user_id=request.user.id, 
            company_id=company_id, 
            form_name=form, 
            data=request.data, 
            public_access_key=request.query_params.get('public_key', None)
        )
        if serializer.is_valid():
            try:
                serializer.save()
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
        GET: gets the data of a form_data_id
        POST: updates a specific form_data_id with new data to a specific form_name
        DELETE: deletes the data of a form_data_id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

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

    def put(self, request, company_id, form, dynamic_form_id):
        duplicate = 'duplicate' in request.query_params
        instance = DynamicForm.objects.filter(id=dynamic_form_id, form__group__company_id=company_id, depends_on__isnull=True).first()
        serializer = FormDataSerializer(
            user_id=request.user.id, 
            company_id=company_id, 
            form_name=form,
            duplicate=duplicate,
            data=request.data,
            instance=instance
        )
        if serializer.is_valid():
            try:
                serializer.save()
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
        GET: This is not a normal API view since it makes a redirection, be aware of that, it's better if you call this
                  in a new tab for the user.
    """
    def get(self, request, company_id, form, dynamic_form_id, field_id, file_name):
        attachment_service = AttachmentService(company_id=company_id, user_id=request.user.id)
        url = attachment_service.get_attachment_url(dynamic_form_id, field_id, file_name)
        if url:
            return redirect(url)
        else:
            return Response({
                'status': 'error'
            })

class APIConfigurationLastValueForFieldDataView(APIView):
    """
    Return the last values by each field he has access to. The idea is that, in the api documentation
    we want to send the actual values to him that he can use this way we can show him a more concise example.

    Methods:
        GET: Return the last inserted values for each field in the formulary to the user.
    """
    def get(self, request, company_id, form):
        formulary_instance = Form.objects.filter(group__company_id=company_id, form_name=form).first()

        if formulary_instance:
            data_service = DataService(request.user.id, company_id)
            last_values_for_field_ids = data_service.get_last_values_for_every_field(formulary_instance)
            serializer = LastValuesSerializer(last_values_for_field_ids, many=True)
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error'
        }, status=status.HTTP_400_BAD_REQUEST)
