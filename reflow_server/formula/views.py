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
        formula_context_for_company = FormulaContextForCompany.objects.filter(company_id=company_id).first() 
        formula_context_attributes = FormulaContextAttributeType.objects.filter(context_type_id=formula_context_for_company.context_type_id).values('attribute_type__name', 'translation')

        formula_attributes = {}
        if formula_context_attributes:
            for formula_context_attribute in formula_context_attributes:
                key = formula_context_attribute['attribute_type__name']
                formula_attributes[key] = formula_context_attribute['translation']

            custom_context = Context(**formula_attributes)
        else:
            custom_context = Context()
        formula_service = FormulaService(text, context=custom_context, dynamic_form_id=dynamic_form_id)
        value = formula_service.evaluate()
        if value in ('#ERROR', '#N/A'):
            return Response({
                'status': 'error'
            }, status=status.HTTP_502_BAD_GATEWAY)
        else:
            return Response({
                'status': 'ok',
                'data': value
            }, status=status.HTTP_200_OK) 

