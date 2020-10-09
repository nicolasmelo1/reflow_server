from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.notification.services.pre_notification import PreNotificationService
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService
from reflow_server.notification.serializers import PreNotificationSerializer, NotificationDataForBuildSerializer, NotificationSerializer, \
    PreNotificationIdsForBuildSerializer


@method_decorator(csrf_exempt, name='dispatch')
class VerifyPreNotificationExternalView(APIView):
    def get(self, request):
        """
        Verify if has a pre_notification configuration to be fired now or less than now

        Methods:
            GET: verify if has a pre_notification to be fired and fires it
        """
        PreNotificationService.verify_pre_notifications()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class PreNotificationExternalView(APIView):
    """
    The pre_notifications update or construction works inside this app, but it is actually
    controlled by celery located in the `REFLOW_WORKER` application. Because when it fails it needs
    to fire the pre_notification again, so, in other words, guarantee that the pre_notification has
    been created.
    That's why we don't use it inside the async function runner inside this application.

    Methods:
        POST: recieves the data and fires a function to update the pre_notifications.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id):
        serializer = PreNotificationSerializer(data=request.data, context={
            'company': company_id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_502_BAD_GATEWAY)


@method_decorator(csrf_exempt, name='dispatch')
class NotificationConfigurationExternalView(APIView):
    """
    This view is used to produce and give the data needed to create the notification.
    Usually this view is used to communicate with the worker to build all the notifications.

    On the other hand this view is also used to effectively create the notifications. The Worker
    build each notification since it's an extensive and heavy task, then when it finishes it 
    sends the data directly to this application.

    Methods:
        POST: gets the data to build the notifications.
        PUT: creates the notifications recieved from the worker.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = PreNotificationIdsForBuildSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.save()
            notification_data_for_build_serializer = NotificationDataForBuildSerializer(data, many=True)

            return Response({
                'status': 'ok',
                'data': notification_data_for_build_serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_502_BAD_GATEWAY)

    def put(self, request):
        serializer = NotificationSerializer(data=request.data, many=True)
        if serializer.is_valid():
            notifications = serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error'
            }, status=status.HTTP_502_BAD_GATEWAY)
