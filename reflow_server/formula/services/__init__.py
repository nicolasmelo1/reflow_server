from django.conf import settings

from reflow_server.data.models import FormValue
from reflow_server.formulary.models import FormulaVariable, FieldType, FieldNumberFormatType
from reflow_server.formula.utils import evaluate
from reflow_server.formula.models import FormulaContextForCompany, FormulaContextAttributeType

import queue
import multiprocessing
import subprocess
import json
import base64
import re


class EvaluationData:
    def __init__(self, status, value):
        self.status = status
        self.value = value


class InternalValue:
    def __init__(self, value, field_type, number_format_type=None, date_format_type=None):
        self.value = value
        self.field_type = field_type
        self.number_format_type = number_format_type
        self.date_format_type = date_format_type
        

class Context:
    def __init__(self, conjunction='and', disjunction='or', inversion='not', 
                 block_do='do', block_end='end', null='None', boolean_true='True',
                 boolean_false='False', if_if='if', if_else='else', function='function',
                 decimal_point_separator='.', positional_argument_separator=','):
        self.data = {
            'keywords': {
                'conjunction': conjunction,
                'disjunction': disjunction,
                'inversion': inversion,
                'null': null,
                'boolean': {
                    'true': boolean_true,
                    'false': boolean_false
                },
                'if': {
                    'if': if_if,
                    'else': if_else
                }, 
                'block': {
                    'do': block_do,
                    'end': block_end
                },
                'function': function,
                'decimal_point_separator': decimal_point_separator,
                'positional_argument_separator': positional_argument_separator
            }
        }


class FormulaService:
    def __init__(self, formula, company_id, dynamic_form_id=None, field_id=None):
        self.__build_context(company_id)
        formula = self.__clean_formula(formula, dynamic_form_id, field_id)
        self.formula = formula
        self.encoded_context = base64.b64encode(json.dumps(self.context.data).encode('utf-8')).decode('utf-8')

    def __build_context(self, company_id):
        """
        This builds the context, the context is a way that we use to translate the formula for many languages like
        portuguese, english, spanish and others. The idea is that the formulas needed to be translatable so it is easier 
        to use for people that do not live in countries like united states, canada. So it becomes easier for non programmers
        to program something complex using our formulas.

        Args:
            company_id (int): A Company instance id
        """
        formula_context_for_company = FormulaContextForCompany.formula_.formula_context_for_company_by_company_id(company_id)
        formula_context_attributes = FormulaContextAttributeType.objects.filter(context_type_id=formula_context_for_company.context_type_id).values('attribute_type__name', 'translation')

        formula_attributes = {}
        if formula_context_attributes:
            for formula_context_attribute in formula_context_attributes:
                key = formula_context_attribute['attribute_type__name']
                formula_attributes[key] = formula_context_attribute['translation']

            self.context = Context(**formula_attributes)
        else:
            self.context = Context()

    def __clean_formula(self, formula, dynamic_form_id, field_id):
        variables = re.findall(r'{{\w*?}}', formula, re.IGNORECASE)
        formula_variables = FormulaVariable.formula_.formula_variables_by_field_id(field_id)
        for index, formula_variable in enumerate(formula_variables):
            values = FormValue.formula_.values_and_field_type_by_main_formulary_data_id_and_field_id(
                dynamic_form_id,
                formula_variable.variable_id
            )
            print(values[0]['field_type__type'])
            if len(values) == 1:
                handler = getattr(self, '_clean_formula_%s' % values[0]['field_type__type'], None)
                if handler:
                    formula = handler(formula, values[0], variables[index])

        return formula

    def _clean_formula_number(self, formula, value, variable):
        value = value['value']
        value = value if value.isdigit() else '1'
        value = (int(value)/settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT)
        return formula.replace(variable, str('%f' % value).replace('.', self.context.data['keywords']['decimal_point_separator']), 1)

    def _clean_formula_text(self, formula, value, variable):
        value = '"{}"'.format(value['value'])
        return formula.replace(variable, value, 1)
    
    def _clean_formula_option(self, formula, value, variable):
        return self._clean_formula_text(formula, value, variable)

    def evaluate_to_internal_value(self):
        """
        Evaluate the formula and transform the result to internal value.

        Returns:
            reflow_server.formula.services.InternalValue: Returns a handy internal value object with the value, the field type
                                                          and the number format type and so on.
        """
        result = self.evaluate()
        result = self.to_internal_value(result)
        return result

    def to_internal_value(self, formula_result):
        """
        Transform the result of the formula to internal value accepted by reflow. In other words we convert the 
        int to a number with the DEFAULT_BASE_NUMBER_FIELD_FORMAT settings. We format the settings and so on. 
        Since formulas are dynamically evaluated we evaluate automatically the type retrieved by the formula to the 
        field type reflow accept.

        Args:
            formula_result (reflow_server.formula.services.EvaluationData): Usually a Evaluation object with the status and a value
                                                                            key that can hold a string
                                                                            or the object retrieved from the formula evaluation
                                                                            of the result and the actual machine value

        Returns:
            reflow_server.formula.services.InternalValue: Returns a handy internal value object with the value, the field type
                                                          and the number format type and so on.
        """
        default_field_type = FieldType.objects.filter(type='text').first()

        is_a_known_and_valid_reflow_formula_object = formula_result.status == 'ok' and hasattr(formula_result.value, 'type')
        if is_a_known_and_valid_reflow_formula_object:
            handler = getattr(self, '_to_internal_value_%s' % formula_result.type, None)
            if handler:
                return handler(formula_result)               
        elif formula_result.status == 'error':
            return InternalValue('#N/A' if formula_result.value == 'Unknown' else '#ERROR', field_type=default_field_type)
    
        return InternalValue('', default_field_type)

    def _to_internal_value_int(self, formula_result):
        field_type = FieldType.objects.filter(type='number').first()
        number_format_type = FieldNumberFormatType.objects.filter(type='number').first()
        value = formula_result._representation_() * settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT

        return InternalValue(value, field_type, number_format_type=number_format_type)

    def _to_internal_value_float(self, formula_result):
        field_type = FieldType.objects.filter(type='number').first()
        number_format_type = FieldNumberFormatType.objects.filter(type='number').first()
        splitted_value = str(formula_result._representation_() * settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT).split('.')
        value = splitted_value[0]     

        return InternalValue(value, field_type, number_format_type=number_format_type)

    def _to_internal_value_string(self, formula_result):
        field_type = FieldType.objects.filter(type='text').first()
        value = formula_result._representation_()

        return InternalValue(value, field_type)

    def __evaluate(self, formula, result):
        try:
            result.put({
                'status': 'ok',
                'value': evaluate(formula)
            })
        except Exception as e:
            result.put({
                'status': 'error',
                'value': str(e)
            })


    def evaluate(self):
        try: 
            result = multiprocessing.Queue()
            process = multiprocessing.Process(target=self.__evaluate, args=(self.formula, result))
            process.start()
            process.join(settings.FORMULA_MAXIMUM_EVAL_TIME/2)
            if process.is_alive():
                process.terminate()
            result = result.get(timeout=settings.FORMULA_MAXIMUM_EVAL_TIME/2)
            return EvaluationData(result['status'], result['value'])
        except queue.Empty as qe:
            return EvaluationData('error', 'Took too long')
        except Exception as e:
            return EvaluationData('error', 'Unknown error')

