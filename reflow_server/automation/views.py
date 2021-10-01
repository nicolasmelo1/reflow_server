from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.automation.models import AutomationApp, AutomationInputFormulary
from reflow_server.automation.services import AutomationService
from reflow_server.automation.serializers import AutomationAppsSerializer, AutomationInputFormularySerializer
from reflow_server.authentication.models import UserExtended


@method_decorator(csrf_exempt, name='dispatch')
class AutomationWebhookVersion1View(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, app_name, automation_trigger_name, user_id):
        company_id = UserExtended.objects.filter(id=user_id).values_list('company_id', flat=True).first()
        if company_id:
            automation_service = AutomationService(company_id)
            automation_service.trigger(user_id=user_id, app_name=app_name, trigger_name=automation_trigger_name, trigger_data=request.data)

        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class AutomationSettingsAppsView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        automation_instances = AutomationApp.objects.all()
        serializer = AutomationAppsSerializer(instance=automation_instances, many=True)

        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class AutomationSettingsInputFormularyView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, input_formulary_id):
        automation_input_instance = AutomationInputFormulary.objects.filter(id=input_formulary_id).first()
        if automation_input_instance:
            serializer = AutomationInputFormularySerializer(instance=automation_input_instance)
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)