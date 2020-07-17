from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.billing.services import VindiService


@method_decorator(csrf_exempt, name='dispatch')
class VindiWebhookView(APIView): 
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        pass


@method_decorator(csrf_exempt, name='dispatch')
class GetTotalView(APIView): 
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        vindi_service = VindiService(1)
        vindi_service.update()
        return Response({
            'status': 'ok'
        })