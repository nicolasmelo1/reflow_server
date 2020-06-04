from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.notification.models import NotificationConfiguration
from reflow_server.notification.services.notification_configuration import NotificationConfigurationService
from reflow_server.formulary.models import Field
from reflow_server.notification.serializers import NotificationConfigurationSerializer, NotificationConfigurationFieldsSerializer


@method_decorator(csrf_exempt, name='dispatch')
class NotificationConfigurationEditView(APIView):
    """
    A view used to edit a notification_configuration_id, it is used to edit a
    notification configuration and to delete a notification_configuration_id only.

    Methods:
        .delete() -- delete an specific notification_configuration_id
        .put() -- edit a notification_configuration_id with new data
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def delete(self, request, company_id, notification_configuration_id):
        NotificationConfigurationService.remove_notification_configuration(user_id=request.user.id, notification_configuration_id=notification_configuration_id)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)

        
    def put(self, request, company_id, notification_configuration_id):
        instance = NotificationConfiguration.objects.filter(id=notification_configuration_id).first()
        serializer = NotificationConfigurationSerializer(data=request.data, instance=instance, context={
            'company_id': company_id,
            'user_id': request.user.id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class NotificationConfigurationView(APIView):
    """
    View that handles retriaval of a list of notification configurations and the creation a SINGLE notification
    configuration

    Methods:
        .get() -- Retrieves a list of notifications configurations that a user has access to for the current company.
        .post() -- Creates a single notification configuration for the user.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        user_notification_configurations = NotificationConfiguration.objects.filter(user_id=request.user.id, user__company_id=company_id)
        notification_configuration_serializer = NotificationConfigurationSerializer(many=True, instance=user_notification_configurations)
        return Response({
            'status': 'ok',
            'data': notification_configuration_serializer.data
        })

    def post(self, request, company_id):
        serializer = NotificationConfigurationSerializer(data=request.data, context={
            'company_id': company_id,
            'user_id': request.user.id
        })
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class NotificationConfigurationFieldsView(APIView):
    """
    Returns all of the possible fields to be used as variables, and to be used on the notification_configuration.
    Right now the fields used for notification_configuration needs to be only of field_type `date`

    Methods:
        .get() -- Returns all of the possible fields to be used as variables, and to be used on the notification_configuration.
    """
    def get(self, request, company_id, form_id):
        serializer = NotificationConfigurationFieldsSerializer(form_id=form_id, company_id=company_id)
        return Response({
            'status': 'ok',
            'data': serializer.data
        })
