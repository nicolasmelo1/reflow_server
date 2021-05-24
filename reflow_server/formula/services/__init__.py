from reflow_server.formula.services.formula import FormulaService

from django.conf import settings

import subprocess
import json
import base64


class FormulaService:
    def __init__(self, formula, context=None, dynamic_form_id=None):
        self.encoded_formula = base64.b64encode(formula.encode('utf-8')).decode('utf-8')
        self.dynamic_form_id = dynamic_form_id

    def evaluate(self):
        try: 
            directory = settings.BASE_DIR
            command = ['node', '%s/extensions/reflow_formula_field/fromCommandLine.js' % (directory) , self.encoded_formula]
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, timeout=10)
            data = json.loads(output)
            return data
        except subprocess.TimeoutExpired as te:
            return '#ERROR'
        except Exception as e:
            return '#N/A'
