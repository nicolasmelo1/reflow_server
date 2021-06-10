from django.conf import settings

from reflow_server.data.models import FormValue
from reflow_server.formulary.models import FormulaVariable

import logging
import subprocess
import json
import base64
import re


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
    def __init__(self, formula, context=None, dynamic_form_id=None, field_id=None):
        if context == None:
            self.context = Context()
        else:
            self.context = context
        formula = self.__clean_formula(formula, dynamic_form_id, field_id)
        self.encoded_formula = base64.b64encode(formula.encode('utf-8')).decode('utf-8')
        self.encoded_context = base64.b64encode(json.dumps(self.context.data).encode('utf-8')).decode('utf-8')

    def __clean_formula(self, formula, dynamic_form_id, field_id):
        variables = re.findall(r'{{\w*?}}', formula, re.IGNORECASE)
        formula_variables = FormulaVariable.formula_.formula_variables_by_field_id(field_id)
        for index, formula_variable in enumerate(formula_variables):
            values = FormValue.formula_.values_and_field_type_by_main_formulary_data_id_and_field_id(
                dynamic_form_id,
                formula_variable.variable_id
            )
            if len(values) == 1:
                if values[0]['field_type__type'] == 'number':
                    value = values[0]['value']
                    value = value if value.isdigit() else '1'
                    value = (int(value)/settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT)
                    formula = formula.replace(variables[index], str('%f' % value).replace('.', self.context.data['keywords']['decimal_point_separator']), 1)
        return formula

    def evaluate(self):
        try: 
            directory = settings.BASE_DIR
            command = ['node', '%s/extensions/reflow_formula_field/fromCommandLine.js' % (directory) , self.encoded_formula, self.encoded_context]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=settings.FORMULA_MAXIMUM_EVAL_TIME)
            logging.error(command)
            data = json.loads(output)
            return data
        except subprocess.TimeoutExpired as te:
            return '#ERROR'
        except Exception as e:
            print(e)
            return '#N/A'
