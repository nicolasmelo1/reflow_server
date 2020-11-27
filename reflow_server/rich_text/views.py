from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.rich_text.serializers import PageSerializer
from reflow_server.rich_text.models import TextPage

@method_decorator(csrf_exempt, name='dispatch')
class TestTextView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, page_id):
        instance = TextPage.objects.filter(id=page_id).first()
        serializer = PageSerializer(instance=instance)
        
        return Response({
            'status': 'ok',
            'data': serializer.data
        })

    