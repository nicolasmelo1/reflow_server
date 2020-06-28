from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.data.services.aggregation import AggregationService
from reflow_server.dashboard.serializers import DashboardDataSerializer, \
    DashboardChartConfigurationSerializer, DashboardFieldsSerializer
from reflow_server.dashboard.models import DashboardChartConfiguration
from reflow_server.formulary.models import Field


class DashboardChartConfigurationView(APIView):
    def get(self, request, company_id, form):
        instances = DashboardChartConfiguration.objects.filter(user_id=request.user.id, company_id=company_id)
        serializer = DashboardChartConfigurationSerializer(instance=instances, many=True)
        #aggregation_service = AggregationService(user_id=1, company_id=1, form_id=21)
        #dashboard_data = aggregation_service.aggregate(method=method_type, field_id_key=49, field_id_value=2284, formated=True)
        #serializer = DashboardDataSerializer(dashboard_data)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class DashboardFieldsView(APIView):
    def get(self, request, company_id, form):
        instances = Field.objects.filter(
            form__depends_on__form_name=form, 
            enabled=True,
            form__enabled=True,
            form__depends_on__group__company_id=company_id
        )
        serializer = DashboardFieldsSerializer(instance=instances, many=True)

        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)