from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.listing.serializers import ExtractDataSerializer


@method_decorator(csrf_exempt, name='dispatch')
class ExtractDataBuilderView(APIView):
    """
    see reflow_server.listing.views.ExtractDataView for further reference.

    View that is used to extract the data from form data. Okay, but how this works?

    The creation of the data to be extracted is asyncronous, what does this mean? You actually fire the request to
    build the data but you do not get the response right away.

    Because of this the HTTP methods are handled the other way around. First you send a post request to build and 
    to create the file, then the file is saved as base64 in our database.

    Methods:
        .post() -- fires the method to build the base64 file.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, form):
        serializer = ExtractDataSerializer(data=request.data, user_id=request.user.id, company_id=company_id, form_name=form)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        return Response({
            'status': 'error'
        }, status=status.HTTP_502_BAD_GATEWAY)


class GetExtractDataView(APIView):
    """
    see reflow_server.listing.views.ExtractDataBuilderView for further reference.

    To extract the data you actually don't need the formulary name because this way you can request to see if there
    are any files ready from anywhere and from any page.

    When the file data is saved you can download the file from our database with the GET method using
    the `download` query parameter.

    When you request the download of the data, we convert the base64 to he desired format you want the data and
    send you the file with all of the data.

    Methods:
        .get() -- Usually returns a JSON saying if your data is ready to be downloaded or not. If it is you
                  need to add the `download` query parameter to your request to download the file
    """
    def get(self, request, company_id):
        return Response({
            'status': 'ok'
        })
