from rest_framework.response import Response
from rest_framework.views import APIView

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.notification.models import UserNotification, NotificationConfiguration
from reflow_server.notification.services.notification import NotificationService
from reflow_server.notification.serializers import UnreadAndReadNotificationSerializer, NotificationConfigurationSerializer


class Notifications(APIView):
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
        })


@method_decorator(csrf_exempt, name='dispatch')
class UnreadAndReadNotification(APIView):
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
        })

    def post(self, request, company_id):
        serializer = UnreadAndReadNotificationSerializer(data=request.data, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 'ok'
        })


@method_decorator(csrf_exempt, name='dispatch')
class APIEditNotificationConfiguration(APIView):
    def delete(self, request, company_id, notification_configuration_id):
        NotificationConfiguration.objects.filter(user_id=request.user.id, id=notification_configuration_id).delete()
        return Response({
            'status': 'ok'
        })

        
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
            })
        else:
            return Response({
                'status': 'error',
                'error': serializer.errors
            }, status=400)