from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.data.models import DynamicForm
from reflow_server.formula.services import FormulaService, Context

class TestNewFormulaView(APIView):
    def get(self, request):
        custom_context = Context(
            conjunction='e',
            disjunction='ou'
        )
        formula_service = FormulaService("""
            1 + 2
        """, context=custom_context)
        value = formula_service.evaluate()
        return Response({
            'status': 'ok',
            'data': value
        }) 


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
        dynamic_form_id = DynamicForm.formula_.latest_main_dynamic_form_id_by_form_id(form_id)
        text = request.GET.get('text')
        formula = FormulaService(text, dynamic_form_id=dynamic_form_id)
        value = formula.evaluate()
        if value in ('#ERROR', '#N/A'):
            return Response({
                'status': 'error'
            }, status=502)
        else:
            return Response({
                'status': 'ok',
                'value': value
            })
