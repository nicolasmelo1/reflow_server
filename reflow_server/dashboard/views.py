from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.data.services.aggregation import AggregationService
from reflow_server.dashboard.serializers import DashboardDataSerializer


class TestAggregation(APIView):
    def get(self, request, method_type):
        aggregation_service = AggregationService(user_id=1, company_id=1, form_id=21)
        dashboard_data = aggregation_service.aggregate(method=method_type, field_id_key=49, field_id_value=2284, formated=True)
        serializer = DashboardDataSerializer(dashboard_data)
        return Response({
            'status': 'ok',
            'data': serializer.data
        })
        