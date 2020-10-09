from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.notify.serializers import PushNotificationRegistrationSerializer


@method_decorator(csrf_exempt, name='dispatch')
class RegisterPushNotificationEndpointView(APIView):
    """
    Register push notification endpoint on the backend. With this we can send push notifications to the user.

    Methods:
        POST: add push notification endpoint to the database bounded to an user.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = PushNotificationRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request.user.id)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
