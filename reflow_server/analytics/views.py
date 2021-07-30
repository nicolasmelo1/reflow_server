from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.events import Event

@method_decorator(csrf_exempt, name='dispatch')
class TrackView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request):
        Event.register_event('formulary_data_created', {
            'user_id': 1,
            'company_id': 1,
            'form_id': 332,
            'form_data_id': 3
        })

        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)