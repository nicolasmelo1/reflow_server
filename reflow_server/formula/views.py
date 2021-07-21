from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.data.models import DynamicForm
from reflow_server.formula.services import FormulaService, FormulaVariables
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
                variables.add_variable_id(variable_id)
            dynamic_form_id = DynamicForm.formula_.latest_main_dynamic_form_id_by_form_id(form_id)
            formula_service = FormulaService(
                serializer.data['formula'], 
                company_id, 
                dynamic_form_id=dynamic_form_id, 
                formula_variables=variables
            )
            value = formula_service.evaluate()
            
            if value.status == 'error':
                return Response({
                    'status': 'error',
                    'error': value.value
                }, status=status.HTTP_502_BAD_GATEWAY)
            else:
                return Response({
                    'status': 'ok',
                    'data': {
                        'result': str(value.value._representation_()) if hasattr(value.value, '_representation_') else ''
                    }
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'error': 'Unknown error'
            }, status=status.HTTP_502_BAD_GATEWAY)

