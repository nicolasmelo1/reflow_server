from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.notification.services.notification import NotificationService
from reflow_server.notification.serializers import UserNotificationSerializer, UnreadAndReadNotificationSerializer

from .external import VerifyPreNotificationExternalView, NotificationConfigurationExternalView, PreNotificationExternalView
from .settings import NotificationConfigurationEditView, NotificationConfigurationFieldsView, NotificationConfigurationView


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
        notifications = UserNotificationSerializer(instance=response.user_notifications, many=True, context={'user': request.user})
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
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id):
        return Response({
            'status': 'ok',
            'data': NotificationService.get_user_new_notifications_number(request.user.id)
        }, status=status.HTTP_200_OK)

    def post(self, request, company_id):
        serializer = UnreadAndReadNotificationSerializer(data=request.data, context={'user_id': request.user.id})
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
