from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.authentication.serializers.settings import CompanySettingsSerializer, UserSettingsSerializer, \
    FormularyAndFieldOptionsSerializer
from reflow_server.authentication.models import Company, UserExtended
from reflow_server.authentication.services.users import UsersService
from reflow_server.formulary.models import Group


@method_decorator(csrf_exempt, name='dispatch')
class CompanySettingsView(APIView):
    """
    This view is responsible to send and recieve data about the company so the admin users can edit it.

    Methods:
        .get() -- Gets all of the data of a company
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        instance = Company.objects.filter(id=company_id).first()
        serializer = CompanySettingsSerializer(instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserSettingsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        instances = UserExtended.objects.filter(company_id=company_id, is_active=True).order_by('-id')
        serializer = UserSettingsSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, company_id):
        serializer = UserSettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class UserSettingsEditView(APIView):
    """
    View responsible for updating a user and deleting a single user. It's important to notice that the user cannot edit or delete itself.

    Methods:
        .put() -- Edits a single user id adding new permissions to the user as well as changing profile types.
        .delete() -- Deletes a single user from the database.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, user_id):
        instance = UserExtended.objects.filter(company_id=company_id, id=user_id, is_active=True).first()
        serializer = UserSettingsSerializer(data=request.data, instance=instance)
        if not UsersService.is_self(int(user_id), int(request.user.id)) and serializer.is_valid():
            serializer.save(company_id)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        elif UsersService.is_self(int(user_id), int(request.user.id)):
            return Response({
                'status': 'error',
                'error': {
                    'detail': ['cannot_edit_itself']
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'status': 'error',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, user_id):
        if not UsersService.is_self(int(user_id), int(request.user.id)):
            UserExtended.objects.filter(company_id=company_id, id=user_id, is_active=True).delete()
            UsersService(company_id).remove_user()
        if UsersService.is_self(int(user_id), int(request.user.id)):
            return Response({
                'status': 'error',
                'error': {
                    'detail': ['cannot_edit_itself']
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
        
        
class FormularyAndFieldOptionsView(APIView):
    def get(self, request, company_id):
        instances = Group.objects.filter(company_id=company_id)
        serializer = FormularyAndFieldOptionsSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)