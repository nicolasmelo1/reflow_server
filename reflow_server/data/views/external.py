from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.data.serializers.extract import ExtractFileSerializer
from reflow_server.data.services.api import APIService


@method_decorator(csrf_exempt, name='dispatch')
class ExtractFileExternalView(APIView):
    """
    View used for recieving the file as a base64 string from the reflow_worker application
    after the file has been built. When we recieve we save the base64 string to our database to 
    be downloaded later by the user.

    We need to use View instead of the APIView here because we got an 415 HTTP ERROR when using 
    a APIView, this happens because we don't set the `content-type` on the header and then this 
    view don't know how to parse and gives errors.

    Methods:
        POST: recieves the data as json inside of the body
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, user_id, form_name):
        serializer = ExtractFileSerializer(data=request.data, user_id=user_id, company_id=company_id, form_name=form_name)
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class APIExternalView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, form_name):
        api_service = APIService(company_id, request.user.id)
        data = request.data        
        if api_service.validate_formulary_name(form_name):
            api_service.save(data)
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': {
                    'reason': 'formulary_does_not_exist'
                }
            }, status=status.HTTP_403_FORBIDDEN)