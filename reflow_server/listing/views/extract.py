from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.listing.serializers import ExtractDataSerializer
from reflow_server.listing.models import ExtractFileData

from datetime import datetime
import io
import csv
import copy
import base64
import xlwt


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
        POST: fires the method to build the base64 file.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, form):
        serializer = ExtractDataSerializer(data=request.data, user_id=request.user.id, company_id=company_id, form_name=form)
        if serializer.is_valid():
            file_id = serializer.save()
            return Response({
                'status': 'ok',
                'data': {
                    'file_id': file_id
                }
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
        GET: Usually returns a JSON saying if your data is ready to be downloaded or not. If it is you
                  need to add the `download` query parameter to your request to download the file
    """
    def get(self, request, company_id, file_id):
        download = request.GET.get('download', None)
        file = ExtractFileData.objects.filter(file_id=file_id, company_id=company_id, user=request.user).first()
        if file and not download:
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        elif file and download == 'download': 

            file_data = copy.deepcopy(file.file)
            file_format = copy.deepcopy(file.file_format)
            form_name = copy.deepcopy(file.form.form_name)
            username = copy.deepcopy(file.user.username)

            file_data = base64.b64decode(file_data)
            file.delete()

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="{}-{}-{}.csv"'.format(form_name, username, datetime.now())
            
            buff = io.StringIO(file_data.decode('utf-8'))
            reader = csv.reader(buff)
            data = copy.deepcopy(list(reader))
            writer = csv.writer(response)
            writer.writerows(data)
            
            if file_format == 'xlsx':
                response = HttpResponse(content_type='application/ms-excel')
                response['Content-Disposition'] = 'attachment; filename="{}-{}-{}.xls"'.format(form_name, username, datetime.now())
                
                wb = xlwt.Workbook(encoding='utf-8')

                ws = wb.add_sheet("Sheet1")

                # Bold Headers
                font_style = xlwt.XFStyle()
                font_style.font.bold = True

                for col_num, column in enumerate(data[0]):
                    ws.write(0, col_num, column, font_style)

                font_style = xlwt.XFStyle()

                for row_num, row in enumerate(data[1:]):
                    for col_num, column in enumerate(row):
                        ws.write(row_num+1, col_num, column, font_style)
        
                wb.save(response)

            return response
        else:
            return Response({
                'status': 'empty'
            }, status=status.HTTP_200_OK)
