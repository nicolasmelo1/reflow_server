from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.core.utils.asynchronous import RunAsyncFunction
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.automation.services import AutomationService
from reflow_server.authentication.models import UserExtended


@method_decorator(csrf_exempt, name='dispatch')
class AutomationWebhookVersion1View(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, app_name, automation_trigger_name, user_id):
        company_id = UserExtended.objects.filter(id=user_id).values_list('company_id', flat=True).first()
        if company_id:
            automation_service = AutomationService(company_id)
            async_function = RunAsyncFunction(automation_service.trigger)
            async_function.delay(user_id=user_id, app_name=app_name, trigger_name=automation_trigger_name, trigger_data=request.data)

        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
