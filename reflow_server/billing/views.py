from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.authentication.models import Company, AddressHelper
from reflow_server.billing.services import VindiService
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.billing.serializers import CurrentCompanyChargeSerializer, PaymentSerializer, \
    AddressOptionsSerializer


class AddressOptionsView(APIView):
    def get(self, request, company_id):
        instance = AddressHelper.objects.all()
        serializer = AddressOptionsSerializer(instance=instance, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class BillingSettingsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        instance = Company.objects.filter(id=company_id).first()
        serializer = PaymentSerializer(instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class VindiWebhookExternalView(APIView): 
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        pass
