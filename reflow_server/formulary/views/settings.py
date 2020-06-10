from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.formulary.serializers.settings import GroupSerializer, FormularySerializer, \
    SectionSerializer
from reflow_server.formulary.models import Group, Form


class GroupSettingsView(APIView):
    def get(self, request, company_id):
        instances = Group.objects.filter(company=company_id)
        serializer = GroupSerializer(instance=instances, many=True, context={
            'company_id': company_id,
            'user_id': request.user.id
        })
        return Response({
            'status': 'ok',
            'data': serializer.data
        })


@method_decorator(csrf_exempt, name='dispatch')
class GroupEditSettingsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, group_id):
        instance = Group.objects.filter()
        serializer = GroupSerializer(instance=instance, data=request.data, context={
            'company_id': company_id,
            'user_id': request.user.id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_200_OK)

    def delete(self, request, company_id, group_id):
        instance = Group.objects.filter(id=group_id, company_id=company_id).first()
        if instance:
            instance.delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class FormularySettingsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id):
        serializer = FormularySerializer(data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class FormularySettingsEditView(APIView):
    """
    This view is used for editing a single formulary and for loading the formulary contents, 
    with all of it's sections and fields.

    Methods:
        .get() -- retrieves the data of the formulary containing all of it's sections and fields
        .put() -- edit a single formulary data (the section can be omitted)
        .delete() -- deletes a single formulary id
    """
    authentication_classes = [CsrfExemptSessionAuthentication]
    
    def get(self, request, company_id, form_id):
        instance = Form.objects.filter(id=form_id, group__company_id=company_id, depends_on__isnull=True).first()
        serializer = FormularySerializer(instance=instance, is_loading_sections=True, context={
            'user_id': request.user.id,
            'company_id': company_id
        })
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, company_id, form_id):
        instance = Form.objects.filter(id=form_id, group__company_id=company_id, depends_on__isnull=True).first()
        serializer = FormularySerializer(instance=instance, data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'ok',
            'data': None
        }, status=status.HTTP_200_OK)

    def delete(self, request, company_id, form_id):
        instance = Form.objects.filter(id=form_id, group__company_id=company_id, depends_on__isnull=True).first()
        if instance:
            instance.delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class SectionSettingsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, form_id):
        serializer = SectionSerializer(data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id,
            'form_id': form_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class SectionSettingsEditView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, form_id, section_id):
        instance = Form.objects.filter(
            id=section_id, 
            group__company_id=company_id, 
            depends_on_id=form_id
        ).first()
        serializer = SectionSerializer(instance=instance, data=request.data, context={
            'user_id': request.user.id,
            'company_id': company_id,
            'form_id': form_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'data': None
            }, status=status.HTTP_200_OK)

    def delete(self, request, company_id, form_id, section_id):
        instance = Form.objects.filter(
            id=section_id, 
            group__company_id=company_id, 
            depends_on_id=form_id
        ).first()
        if instance:
            instance.delete()
            
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)