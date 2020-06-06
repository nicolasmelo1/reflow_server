from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View

from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.listing.serializers import ExtractFileSerializer

import json


@method_decorator(csrf_exempt, name='dispatch')
class ExtractFileExternalView(View):
    """
    View used for recieving the file as a base64 string from the reflow_worker application
    after the file has been built. When we recieve we save the base64 string to our database to 
    be downloaded later by the user.

    We need to use View instead of the APIView here because we got an 415 HTTP ERROR when using 
    a APIView, this happens because we don't set the `content-type` on the header and then this 
    view don't know how to parse and gives errors.

    Methods:
        .post() -- recieves the data as json inside of the body
    """
    def post(self, request, company_id, user_id, form_name):
        data = json.loads(request.body.decode('utf-8'))
        serializer = ExtractFileSerializer(data=data, user_id=user_id, company_id=company_id, form_name=form_name)
        if serializer.is_valid():
            serializer.save()
        return JsonResponse({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
