from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.data.services.aggregation import AggregationService
from reflow_server.dashboard.serializers import DashboardDataSerializer, \
    DashboardChartConfigurationSerializer, DashboardFieldsSerializer, DashboardChartSerializer
from reflow_server.dashboard.models import DashboardChartConfiguration
from reflow_server.formulary.models import Field, Form

from datetime import datetime


class DashboardDataView(APIView):
    """
    This view is responsible for effectively serving the data of a particular dashboard_id.
    When you send the dashboard_id to this view this automatically gets the data of this dashboard
    for you.

    This means that usually you can't access the aggregated data directly by any API but instead, 
    need to have configurated a new chart in order to get the aggregated data.

    Method:
        .get() -- Returns the aggregated data with `labels` being a list and `values` being a list 
                  also, both lists needs to have the same size.
    """
    def get(self, request, company_id, form, dashboard_configuration_id):
        form_id = Form.objects.filter(form_name=form, company_id=company_id).values_list('id', flat=True).first()
        instance = DashboardChartConfiguration.objects.filter(id=dashboard_configuration_id, company_id=company_id).first()

        aggregation_service = AggregationService(
            user_id=request.user.id, 
            company_id=company_id, 
            form_id=form_id, 
            query_params=request.query_params
        )
        dashboard_data = aggregation_service.aggregate(
            method=instance.aggregation_type.name, 
            field_id_key=instance.label_field.id, 
            field_id_value=instance.value_field.id, 
            formated=True)
        serializer = DashboardDataSerializer(dashboard_data)
        return Response({
                'status': 'ok',
                'data': serializer.data
        }, status=status.HTTP_200_OK)


class DashboardChartsView(APIView):
    """
    View responsible for retrieving all of the dashboards to load when not updating
    the charts. So this view actually retrieves the charts for the user to load the data.

    Methods:
        .get() -- retrive the charts to load for the specific user and the specific form 
                  for the specific company
    """
    def get(self, request, company_id, form):
        instances = DashboardChartConfiguration.objects.filter(
            Q(user_id=request.user.id, form__form_name=form, company_id=company_id) | 
            Q(company_id=company_id, form__form_name=form, for_company=True)
        )
        serializer = DashboardChartSerializer(instance=instances, many=True)

        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class DashboardChartConfigurationView(APIView):
    """
    View responsible for retriving a list of the charts that a specific user can edit and also
    for creating a single chart for the user.

    Methods:
        .get() -- retrieve a list of charts that the user can edit (the ones that the user have created)
        .post() -- creates a new chart for the user
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def get(self, request, company_id, form):
        instances = DashboardChartConfiguration.objects.filter(
            user_id=request.user.id, 
            form__form_name=form, 
            company_id=company_id
        ).order_by('-id')
        serializer = DashboardChartConfigurationSerializer(instance=instances, many=True)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request, company_id, form):
        form_id = Form.objects.filter(form_name=form, company_id=company_id).values_list('id', flat=True).first()
        serializer = DashboardChartConfigurationSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(company_id, form_id, request.user.id)
            serializer = DashboardChartConfigurationSerializer(instance=instance)
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class DashboardChartConfigurationEditView(APIView):
    """
    View responsible for handling edition of charts configurations, this means update and 
    deletion of a chart in the users dashboard.

    Methods:
        .put() -- Edits an chart instance
        .delete() -- Deletes an chart instance
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, form, dashboard_configuration_id):
        form_id = Form.objects.filter(form_name=form, company_id=company_id).values_list('id', flat=True).first()
        instance = DashboardChartConfiguration.objects.filter(user_id=request.user.id, form__form_name=form, company_id=company_id, id=dashboard_configuration_id).first()
        serializer = DashboardChartConfigurationSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            instance = serializer.save(company_id, form_id, request.user.id)
            serializer = DashboardChartConfigurationSerializer(instance=instance)
            return Response({
                'status': 'ok',
                'data': serializer.data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'ok',
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, company_id, form, dashboard_configuration_id):
        instance = DashboardChartConfiguration.objects.filter(user_id=request.user.id, form__form_name=form, company_id=company_id, id=dashboard_configuration_id)
        if instance:
            instance.delete()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


class DashboardFieldsView(APIView):
    """
    When the user edits a chart he needs to define the label_field and also
    the value_field. This is why this view actually exists, to retrieve the fields
    he can use to create a new chart. 

    Since charts are bound to a specific formulary, he needs to retrieve the fields only from
    a specific formulary, not all forms

    Methods:
        .get() -- Returns an array of fields
    """
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
