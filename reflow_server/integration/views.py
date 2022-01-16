from re import S
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.integration.serializers import IntegrationAuthenticationSerializer

@method_decorator(csrf_exempt, name='dispatch')
class IntegrationAuthenticationView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, service_name):
        serializer = IntegrationAuthenticationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(service_name, request.user.id)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
