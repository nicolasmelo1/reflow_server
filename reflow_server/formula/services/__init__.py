from django.conf import settings

from reflow_server.data.models import FormValue

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
    def __init__(self, formula, context=None, dynamic_form_id=None):
        if context == None:
            self.context = Context()
        else:
            self.context = context
        formula = self.__clean_formula(formula, dynamic_form_id)
        self.encoded_formula = base64.b64encode(formula.encode('utf-8')).decode('utf-8')
        self.encoded_context = base64.b64encode(json.dumps(self.context.data).encode('utf-8')).decode('utf-8')

    def __clean_formula(self, formula, dynamic_form_id):
        variables = re.findall(r'{{\d+}}', formula, re.IGNORECASE)
        for variable in variables:
            field_id = variable.replace(r'{{', '').replace(r'}}', '')
            values = FormValue.formula_.values_and_field_type_by_main_formulary_data_id_and_field_id(
                dynamic_form_id,
                int(field_id)
            )
            if len(values) == 1:
                if values[0]['field_type__type'] == 'number':
                    value = values[0]['value']
                    value = value if value.isdigit() else '1'
                    value = (int(value)/settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT)/values[0]['number_configuration_number_format_type__base']
                    formula = formula.replace(variable, str('%f' % value).replace('.', self.context.data['keywords']['decimal_point_separator']))
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
