from django.shortcuts import redirect
from django.conf import settings
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.utils.storage import Bucket
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.data.serializers import FormDataSerializer
from reflow_server.data.models import DynamicForm, Attachments

import urllib
import json


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
        data = request.data.pop('data')[0]
        serializer = FormDataSerializer(user_id=request.user.id, company_id=company_id, form_name=form, data=json.loads(data))
        if serializer.is_valid():
            serializer.save(files=[])
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
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
        instance = DynamicForm.objects.filter(
            id=dynamic_form_id, 
            form__group__company_id=company_id, 
            depends_on__isnull=True
        ).first()

        serializer = FormDataSerializer(
            instance=instance,
            user_id=request.user.id, 
            company_id=company_id, 
            form_name=form
        )
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, company_id, form, dynamic_form_id):
        duplicate = request.query_params.get('duplicate', None)
        data = request.data.pop('data')[0]
        serializer = FormDataSerializer(
            user_id=request.user.id, 
            company_id=company_id, 
            form_name=form,
            form_data_id=dynamic_form_id,
            duplicate=duplicate != None,
            data=json.loads(data)
        )
        if serializer.is_valid():
            serializer.save(files=[])
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, form, dynamic_form_id):
        DynamicForm.objects.filter(form__group__company_id=company_id,
                                   form__form_name=form, id=dynamic_form_id).delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)



class DownloadFile(APIView):
    def get(self, request, company_id, form, dynamic_form_id, field_id, file_name):
        depends_on_pk = DynamicForm.objects.filter(pk=dynamic_form_id).first().depends_on_id
        attachment = Attachments.objects.filter(Q(form__depends_on_id=dynamic_form_id) | Q(form_id=dynamic_form_id))\
            .filter(field_id=field_id, file=file_name).first()
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
            