from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.formulary.models import Field
from reflow_server.notification.models import UserNotification, NotificationConfiguration
from reflow_server.notification.services.notification import NotificationService
from reflow_server.notification.serializers import UnreadAndReadNotificationSerializer, NotificationConfigurationSerializer, \
    NotificationSerializer, NotificationFieldsSerializer


@method_decorator(csrf_exempt, name='dispatch')
class NotificationsView(APIView):
    """
    Retrieves all(paginated) of the notifications of a user.

    Methods:
        .get() -- Returns the pagination of all of the notifications and all of the
                  notifications of a user.
    """
    def get(self, request, company_id):
        page = int(request.GET.get('page', '1'))
        response = NotificationService.get_and_update_user_notifications(user_id=request.user.id, page=page)
        notifications = NotificationSerializer(instance=response.user_notifications, many=True, context={'user': request.user})
        return Response({
            'status': 'ok',
            'data': {
                'pagination': {
                    'total': response.total_pages,
                    'current': page
                },
                'data': notifications.data
            }
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UnreadAndReadNotificationView(APIView):
    """
    Handles unread and read notifications, for unread notifications it works on the .get method
    this method only retrieves the number of unread new notifications so we can update the badge
    of new notifications. Secondly it handles read notifications, so when a user read, we send a 
    .post request to update that the user has read the notification id

    Methods:
        .get() -- retrieves the number of new notifications
        .post() -- updates that the user has read the notification id
    """
    def get(self, request, company_id):
        return Response({
            'status': 'ok',
            'data': NotificationService.get_user_new_notifications_number()
        }, status=status.HTTP_200_OK)

    def post(self, request, company_id):
        serializer = UnreadAndReadNotificationSerializer(data=request.data, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class NotificationConfigurationEditView(APIView):
    """
    A view used to edit a notification_configuration_id, it is used to edit a
    notification configuration and to delete a notification_configuration_id only.

    Methods:
        .delete() -- delete an specific notification_configuration_id
        .put() -- edit a notification_configuration_id with new data
    """
    def delete(self, request, company_id, notification_configuration_id):
        NotificationConfiguration.objects.filter(user_id=request.user.id, id=notification_configuration_id).delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)

        
    def put(self, request, company_id, notification_configuration_id):
        instance = NotificationConfiguration.objects.filter(id=notification_configuration_id).first()
        serializer = NotificationConfigurationSerializer(data=request.data, instance=instance, context={
            'company_id': Encrypt.decrypt_pk(company_id),
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
    def get(self, request, company_id):
        user_notification_configurations = NotificationConfiguration.objects.filter(user_id=request.user.id, user__company_id=Encrypt.decrypt_pk(company_id))
        notification_configuration_serializer = NotificationConfigurationSerializer(many=True, instance=notification_configuration_serializer)
        return Response({
            'status': 'ok',
            'data': notification_configuration_serializer.data
        })

    def post(self, request, company_id):
        serializer = NotificationConfigurationSerializer(data=request.data, context={
            'company_id': Encrypt.decrypt_pk(company_id),
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
class NotificationConfigurationFields(View):
    """
    Returns all of the possible fields to be used as variables, and to be used on the notification_configuration.
    Right now the fields used for notification_configuration needs to be only of field_type `date`

    Methods:
        .get() -- Returns all of the possible fields to be used as variables, and to be used on the notification_configuration.
    """
    def get(self, request, company_id, form_id):
        fields = Field.objects.filter(
            form__depends_on_id=form_id, 
            form__depends_on__group__company_id=Encrypt.decrypt_pk(company_id), 
            enabled=True, 
            form__enabled=True, 
            form__depends_on__enabled=True, 
            form__depends_on__group__enabled=True
        )
        notification_fields = NotificationFieldsSerializer(fields.filter(type__type='date'), many=True)
        variable_fields = NotificationFieldsSerializer(fields, many=True)
        return Response({
            'data': {
                'notification_fields': notification_fields.data,
                'variable_fields': variable_fields.data
            }
        })