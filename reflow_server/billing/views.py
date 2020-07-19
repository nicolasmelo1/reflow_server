from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.authentication.models import Company
from reflow_server.billing.services import VindiService
from reflow_server.billing.models import CurrentCompanyCharge
from reflow_server.billing.serializers import CurrentCompanyChargeSerializer, PaymentSerializer


@method_decorator(csrf_exempt, name='dispatch')
class CurrentCompanyChargeView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        instances = CurrentCompanyCharge.objects.filter(company_id=company_id)
        serializer = CurrentCompanyChargeSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentView(APIView):
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


@method_decorator(csrf_exempt, name='dispatch')
class GetTotalView(APIView): 
    authentication_classes = [CsrfExemptSessionAuthentication]
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request, company_id):
        #vindi_service = VindiService(1)
        #vindi_service.update()
        return Response({
            'status': 'ok'
        })

    def post(self, request, company_id):
        return Response({
            'status': 'ok'
        })