from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.authentication.serializers.settings import CompanySettingsSerializer, UserSettingsSerializer
from reflow_server.authentication.models import Company, UserExtended


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


class UserSettingsView(APIView):
    def get(self, request, company_id):
        instances = UserExtended.objects.filter(company_id=company_id)
        serializer = UserSettingsSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def post(self, request, company_id):
        serializer = UserSettingsSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'status': 'error',
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)