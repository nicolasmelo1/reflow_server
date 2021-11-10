from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.analytics.services import AnalyticsService
from reflow_server.analytics.models import Survey
from reflow_server.analytics.serializers import SurveySerializer, SurveyAnswerSerializer
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


@method_decorator(csrf_exempt, name='dispatch')
class SurveyView(APIView):
    """
    View responsible for getting the necessary data needed to display the survey to the user and for saving
    the response of the survey in the database.

    Methods:
        GET: Retrieves the necessary data to build the survey.
        POST: Saves the response of the survey.
    """

    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, survey_id):
        survey = Survey.analytics_.survey_by_id(survey_id)
        if survey:
            serializer = SurveySerializer(instance=survey)
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'reason': 'invalid_survey'
            }, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, survey_id):
        serializer = SurveyAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(survey_id, request.user.id)
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)