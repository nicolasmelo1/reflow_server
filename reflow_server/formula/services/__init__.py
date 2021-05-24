from reflow_server.formula.services.formula import FormulaService

from django.conf import settings

import subprocess
import json

def call_formula(formula_string):
    directory = settings.BASE_DIR
    process = subprocess.Popen(['node', '%s/extensions/reflow_formula_field/main.js' % directory], stdout=subprocess.PIPE)
    out = process.stdout.read()
    data = json.loads(out)
    return data