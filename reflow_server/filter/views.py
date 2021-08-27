from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.filter.services.data import FilterFormularyDataData, FilterConditionData
from reflow_server.filter.services import FilterDataService
from reflow_server.data.models import DynamicForm, FormValue
from reflow_server.formulary.models import Field
from reflow_server.data.services import RepresentationService


class TestSearchFilterView(APIView):
    def get(self, request):
        
        field = Field.objects.filter(id=757).first()
        field2 = Field.objects.filter(id=756).first()

        representation_service = RepresentationService(
            field.type.type,
            field.date_configuration_date_format_type_id,
            field.number_configuration_number_format_type_id,
            field.form_field_as_option_id
        )

        representation_service2 = RepresentationService(
            field.type.type,
            field.date_configuration_date_format_type_id,
            field.number_configuration_number_format_type_id,
            field.form_field_as_option_id
        )

        filter_condition_data = FilterConditionData(
            field, 
            field.type.type, 
            'contains', 
            False,
            representation_service.to_internal_value('Forma')
        )
        filter_condition_data2 = FilterConditionData(
            field2, 
            field2.type.type, 
            'contains', 
            False,
            representation_service2.to_internal_value('test'),
            connector='and'
        )
        
        form_ids_to_filter = DynamicForm.objects.filter(company_id=1, depends_on__isnull=True, form__form_name='eventos').values_list('id', flat=True)
        filter_service = FilterDataService(1)
        data = filter_service.search([filter_condition_data, filter_condition_data2], form_ids_to_filter)
        return Response({
            'status': 'ok',
            'data': data
        }, status=status.HTTP_200_OK)


class TesValidateFilterView(APIView):
    def get(self, request):
        field = Field.objects.filter(id=757).first()
        field2 = Field.objects.filter(id=756).first()

        filter_condition_data = FilterConditionData(
            field, 
            field.type.type, 
            'contains', 
            False,
            'Forma'
        )
        filter_condition_data2 = FilterConditionData(
            field2, 
            field2.type.type, 
            'contains', 
            False,
            'test',
            connector='and'
        )
        last_dynamic_form = DynamicForm.objects.filter(company_id=1, depends_on__isnull=True, form__form_name='eventos').order_by('-updated_at').first()
        form_values_to_filter = FormValue.objects.filter(form__depends_on=last_dynamic_form)

        filter_formulary_data = FilterFormularyDataData()
        for form_value in form_values_to_filter:
            filter_formulary_data.add_value(form_value.field_type.type, form_value.field.name, form_value.value)
        
        filter_service = FilterDataService(1)
        data = filter_service.validate([filter_condition_data, filter_condition_data2], filter_formulary_data)
        return Response({
            'status': 'ok',
            'data': data
        }, status=status.HTTP_200_OK)