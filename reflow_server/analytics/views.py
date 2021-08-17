from reflow_server.analytics.managers import event
from reflow_server.analytics.services import AnalyticsService
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.core.events import Event


@method_decorator(csrf_exempt, name='dispatch')
class TrackView(APIView):
    """
    View responsible for tracking events, on this the user don't need to be logged in. This is for tracking events that are 
    impossible to track only with the backend.

    Methods:
        POST: Track a event, please send the data flat, DO NOT SEND nested data.
              Instead of:
              >>> {
                  'company': {
                      'id': 12,
                      'name': 'Reflow'
                  }
              }
              send something like:
              >>> {
                  'company_id': 12,
                  'company_name': 'Reflow'
              }
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, event_name):
        """
        Tracks external events that cannot be tracked inside of reflow server itself.
        """
        analytics_service = AnalyticsService()
        formated_data = analytics_service.format_request_event(request.data)
        
        try:
            Event.register_event(event_name, data=formated_data)
        
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({
                'status': 'error',
                'reason': 'event_name_not_expected'
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
        except KeyError as ke:
            return Response({
                'status': 'error',
                'reason': 'expected_data_formated_wrong'
            }, status=status.HTTP_501_NOT_IMPLEMENTED)
        except Exception as e:
            return Response({
                'status': 'error',
                'reason': 'unknown'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)