from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.data.models import DynamicForm
from reflow_server.formula.services.formula import FlowFormulaService, FormulaVariables
from reflow_server.formula.serializers import FormulaSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TestFormulaView(APIView):
    """
    This view is used just to validate if a formula is valid or not, we validate using the last
    values inserted from a formulary.

    Query Parameters:
        text -- it is the formula as text to calculate.

    Methods:
        GET: used for validating if a formula is valid or not. If it has a `field` token 
                  (see `reflow_server.formula.utils.token.Token` for reference) it uses the last
                  inserted data of the formulary to validate it. It could use a factory, but we 
                  can do it later.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request, company_id, form_id):
        serializer = FormulaSerializer(data=request.data)
        if serializer.is_valid():
            variables = FormulaVariables()
            for variable_id in serializer.data['variable_ids']:
                if isinstance(variable_id, int) or variable_id.isdigit():
                    variables.add_variable_id(variable_id)
            dynamic_form_id = DynamicForm.formula_.latest_main_dynamic_form_id_by_form_id(form_id)
            formula_service = FlowFormulaService(
                serializer.data['formula'], 
                request.user.id,
                company_id, 
                dynamic_form_id=dynamic_form_id, 
                formula_variables=variables,
                is_testing=True
            )
            value = formula_service.evaluate()
            stringfied_representation = value.value._string_()._representation_() \
                if hasattr(value.value, '_string_') \
                    else str(value.value)
            if value.status == 'error':
                return Response({
                    'status': 'error',
                    'error': str(stringfied_representation)
                }, status=status.HTTP_502_BAD_GATEWAY)
            else:
                return Response({
                    'status': 'ok',
                    'data': {
                        'result': stringfied_representation,
                        'integrations_to_authenticate': [{'service_name': integrations.service_name } 
                            for integrations in formula_service.services_user_needs_to_authenticate]
                    }
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': 'Unknown error'
            }, status=status.HTTP_502_BAD_GATEWAY)


@method_decorator(csrf_exempt, name='dispatch')
class TesteWebhook(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    def post(self, request):
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)
