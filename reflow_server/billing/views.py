from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.authentication.models import Company, AddressHelper
from reflow_server.billing.models import CompanyBilling
from reflow_server.billing.services.data import CompanyChargeData
from reflow_server.billing.services import VindiService, BillingService, ChargeService
from reflow_server.billing.serializers import CurrentCompanyChargeSerializer, PaymentSerializer, \
    AddressOptionsSerializer, TotalsSerializer


class AddressOptionsView(APIView):
    def get(self, request, company_id):
        instance = AddressHelper.billing_.get_all()
        serializer = AddressOptionsSerializer(instance=instance, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class TotalsView(APIView):
    """
    This view gets the total charges. This is used when the user changes a charge 
    value so he can see the right value in real time.

    Methods:
        POST: Gets the total of all of the charges.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id):
        instance = CompanyBilling.objects.filter(company_id=company_id).first()
        serializer = CurrentCompanyChargeSerializer(data=request.data, many=True)
        if serializer.is_valid():
            charge_service = ChargeService(company_id, instance)
            current_company_charges = [
                CompanyChargeData(
                    individual_value_charge_name=current_company_charge['name'], 
                    quantity=current_company_charge['quantity'], 
                    user_id=current_company_charge['user_id']
                ) 
                for current_company_charge in serializer.initial_data
            ]
            total_data = charge_service.get_total_data_from_custom_charge_quantity(current_company_charges)
            data = {
                'total': total_data.total,
                'discounts': total_data.total_coupons_discounts,
                'total_by_name': [{'name': key, 'total': value} for key, value in total_data.total_by_charge_name.items()]
            }
            serializer = TotalsSerializer(data=data)
            return Response({
                'status': 'ok',
                'data': serializer.initial_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_400_BAD_REQUEST)
    

@method_decorator(csrf_exempt, name='dispatch')
class BillingSettingsView(APIView):
    """
    This view is responsible for retrieving billing and updating billing information.
    Usually we separate the billing information in 3 steps: Address, Charge, Payment.
    1 - Address - is the address of the company only used on the billing, only needed for payment
    2 - Charge - This is actually the plan data of the user, this is where he defines what he wants and want to pay. This what
    he usually changes more.
    3 - Payment - The payment information like when he wants to be billed, who he wants to bill and the payment method.

    Methods:
        GET: Retrieves the payment data information containing all of the 3 stuff in the json.
        PUT: Recieves the json and updates the billing information of the user.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        instance = CompanyBilling.objects.filter(company_id=company_id).first()
        serializer = PaymentSerializer(instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def put(self, request, company_id):
        instance = CompanyBilling.objects.filter(company_id=company_id).first()
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
    """
    Used for deleting and removing credit cards of the user from the payment gateway platform.
    For security reasons we don't have any information about the credit card data transactioning our servers.

    Methods:
        DELETE: deletes the credit card data of a user.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def delete(self, request, company_id):
        billing_service = BillingService(company_id)
        billing_service.remove_credit_card()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class VindiWebhookExternalView(APIView): 
    """
    This is an external view, it's not accessed by the client. This view is used for retrieving webhook 
    events from the vindi platform so we can activate or deactivate a user. And so on.

    Methods:
        POST: recieves a post request from the webhook, it's always a POST request
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        secret = request.query_params.get('secret', '')
        if settings.VINDI_WEBHOOK_SECRET_KEY == secret:
            VindiService.handle_webhook(request.data)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)