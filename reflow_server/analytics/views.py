from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.data.services.aggregation import AggregationService


class TestAggregation(APIView):
    def get(self, request):
        aggregation_service = AggregationService(user_id=1, company_id=1, form_id=21)
        return Response({
            'status': 'ok',
            'data': aggregation_service.aggregate(method='sum', field_id_key=49, field_id_value=2284)
        })