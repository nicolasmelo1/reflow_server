from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.filter.services import FilterDataService, FilterConditionData
from reflow_server.data.models import DynamicForm
from reflow_server.formulary.models import Field
from reflow_server.data.services import RepresentationService


class TestarFilter(APIView):
    def get(self, request):
        field = Field.objects.filter(id=758).first()
        representation_service = RepresentationService(
            field.type.type,
            field.date_configuration_date_format_type_id,
            field.number_configuration_number_format_type_id,
            field.form_field_as_option_id
        )

        filter_condition_data = FilterConditionData(
            field, 
            field.type.type, 
            'is_empty', 
            False,
            None
        )
        
        form_ids_to_filter = DynamicForm.objects.filter(company_id=1, depends_on__isnull=True, form__form_name='eventos').values_list('id', flat=True)
        filter_service = FilterDataService(1, form_ids_to_filter)
        data = filter_service.search([filter_condition_data])
        return Response({
            'status': 'ok',
            'data': data
        }, status=status.HTTP_200_OK)