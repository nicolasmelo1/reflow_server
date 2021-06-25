from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.data.models import DynamicForm
from reflow_server.formula.services import FormulaService, Context
from reflow_server.formula.models import FormulaContextAttributeType, FormulaContextForCompany


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
    def get(self, request, company_id, form_id):
        text = request.GET.get('text')

        dynamic_form_id = DynamicForm.formula_.latest_main_dynamic_form_id_by_form_id(form_id)
        formula_service = FormulaService(text, company_id, dynamic_form_id=dynamic_form_id)
        value = formula_service.evaluate()
        if value.status == 'error':
            return Response({
                'status': 'error',
                'error': value.value
            }, status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK) 

