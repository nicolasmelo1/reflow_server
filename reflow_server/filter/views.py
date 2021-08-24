from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.filter.services import FilterDataService, FilterConditionData
from reflow_server.data.models import DynamicForm
from reflow_server.formulary.models import Field


class TestarFilter(APIView):
    def get(self, request):
        field = Field.objects.filter(id=756).first()
        filter_condition_data = FilterConditionData(
            field, 'contains', False, 'casa'
        )
        
        form_ids_to_filter = DynamicForm.objects.filter(company_id=1, depends_on__isnull=True).values_list('id', flat=True)
        filter_service = FilterDataService(form_ids_to_filter)
        filter_service.search([filter_condition_data])
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)