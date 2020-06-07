from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.formulary.serializers import FormDataSerializer

@method_decorator(csrf_exempt, name='dispatch')
class FormularyDataView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, form):
        serializer = FormDataSerializer(user_id=request.user.id, company_id=company_id, form_name=form, data=request.data)
        serializer.is_valid()
        return Response({
            'status': 'ok'
        })