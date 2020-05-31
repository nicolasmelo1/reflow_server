from rest_framework.views import APIView
from rest_framework.response import Response

from reflow_server.formulary.models import DynamicForm
from reflow_server.formula.services import FormulaService


class TestFormula(APIView):
    """
    This view is used just to validate if a formula is valid or not, we validate using the last
    values inserted from a formulary.

    Query Parameters:
        text -- it is the formula as text to calculate.

    Methods:
        .get() -- used for validating if a formula is valid or not. If it has a `field` token 
                  (see `reflow_server.formula.utils.token.Token` for reference) it uses the last
                  inserted data of the formulary to validate it. It could use a factory, but we 
                  can do it later.
    """
    def get(self, request, company_id, form_id):
        dynamic_form_id = DynamicForm.objects.filter(form_id=form_id, depends_on__isnull=True).order_by('-updated_at').values_list('id', flat=True).first()
        text = request.GET.get('text')
        formula = FormulaService(text, dynamic_form_id=dynamic_form_id)
        value = formula.value
        if value in ('#ERROR', '#N/A'):
            return Response({
                'status': 'error'
            }, status=502)
        else:
            return Response({
                'status': 'ok',
                'value': value
            })
