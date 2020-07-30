from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.authentication.models import Company, AddressHelper
from reflow_server.billing.services.data import CompanyChargeData
from reflow_server.billing.services import VindiService, BillingService, ChargeService
from reflow_server.billing.serializers import CurrentCompanyChargeSerializer, PaymentSerializer, \
    AddressOptionsSerializer, TotalsSerializer


class AddressOptionsView(APIView):
    def get(self, request, company_id):
        instance = AddressHelper.objects.all()
        serializer = AddressOptionsSerializer(instance=instance, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class TotalsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id):
        instance = Company.objects.filter(id=company_id).first()
        serializer = CurrentCompanyChargeSerializer(data=request.data, many=True)
        if serializer.is_valid():
            charge_service = ChargeService(instance)
            current_company_charges = [
                CompanyChargeData(
                    individual_value_charge_name=current_company_charge['name'], 
                    quantity=current_company_charge['quantity'], 
                    user_id=current_company_charge['user_id']
                ) 
                for current_company_charge in serializer.initial_data
            ]
            total_data = charge_service.get_total_data_from_custom_charge_quantity(current_company_charges)
            data = [{'name': key, 'total': value} for key, value in total_data.total_by_charge_name.items()]
            serializer = TotalsSerializer(data=data, many=True)
            return Response({
                'status': 'ok',
                'data': serializer.initial_data
            }, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
    

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
    
    def put(self, request, company_id):
        instance = Company.objects.filter(id=company_id).first()
        serializer = PaymentSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except ConnectionError as ce:
                return Response({
                    'status': 'error',
                    'error': {
                        'reason': 'payment_gateway_error'
                    }
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class CreditCardView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def delete(self, request, company_id):
        billing_service = BillingService(company_id)
        billing_service.remove_credit_card()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class VindiWebhookExternalView(APIView): 
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        pass
