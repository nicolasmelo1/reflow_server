from django.conf import settings
from django.db.utils import DEFAULT_DB_ALIAS, load_backend
from django import db

from reflow_server.formula.models import FormulaContextType
from reflow_server.formula.services.data import EvaluationData
from reflow_server.formula.services.utils import build_context
from reflow_server.formula.utils import evaluate

import queue
import multiprocessing

    
def create_connection(alias=DEFAULT_DB_ALIAS):
    db.connections.ensure_defaults(alias)
    db.connections.prepare_test_settings(alias)
    database = db.connections.databases[alias]
    backend = load_backend(database['ENGINE'])
    return backend.DatabaseWrapper(database, alias)


class FlowAutomationService:
    def __init__(self, context_type_id, company_id, user_id, automation_id, trigger_data=None, action_data=None):
        self.company_id = company_id
        self.user_id = user_id
        self.automation_id = automation_id
        self.trigger_data = trigger_data
        self.action_data = action_data

        if context_type_id == None:
            context_type_id = FormulaContextType.objects.filter(name='default').values_list('id', flat=True).first()

        self.context = build_context(context_type_id, 'automation')
        self.context.add_reflow_data(
            company_id, 
            user_id, 
            automation_id=automation_id, 
            automation_trigger_data=trigger_data, 
            automation_action_data=action_data
        )
    # ------------------------------------------------------------------------------------------
    def __evaluate(self, formula, result):
        """
        If on development, we will let the errors occur freely while on production errors should all be supressed Except the ones
        that is from the language itself.

        Args:
            formula (str): The actual formula string
            result (): Where you put the values of the result
        """
        def evaluate_result():
            # okay, so why do we need this you might ask, it is because we were getting the following error 
            # "SSL error: decryption failed or bad record mac django"
            # To solve this i relied on this response: https://stackoverflow.com/a/68849119 simple and elegant
            connection = create_connection()

            formula_result = evaluate(formula, self.context)
            status = 'error' if getattr(formula_result, 'type', '') == 'error' else 'ok'
            result.put({
                'status': status,
                'value': formula_result
            })
            connection.close()
            
        if settings.ENV == 'development':
            evaluate_result()
        else:
            try:
                evaluate_result()
            except Exception as e:
                result.put({
                    'status': 'error',
                    'value': str(e)
                })
    # ------------------------------------------------------------------------------------------
    def evaluate(self, formula):
        """
        The evaluation process is similar as how it was done before making our own programming language.

        It runs inside of a process and you might ask yourself why.

        The idea is simple: if we can run a programming language inside of the server, how to tank the server?
        Simple, just run an infinite loop and tank the server. Also we can add formulas like 1123123123 ^ 123123123123 that
        can take too long. On all of those cases we kill the process when it takes too long.

        Returns:
            reflow_server.formula.services.data.EvaluationData: The Evaluation data is a object we use to retrieve the data and understand
                                                                what we need to evaluate for with the result.
        """             
        def run_evaluation_as_another_process():
            result = multiprocessing.Queue()
            process = multiprocessing.Process(target=self.__evaluate, args=(formula, result))
            process.start()
            process.join(settings.FORMULA_MAXIMUM_EVAL_TIME/2)
            if process.is_alive():
                process.terminate()
            result = result.get(timeout=settings.FORMULA_MAXIMUM_EVAL_TIME/2)
            return EvaluationData(result['status'], result['value'])

        if settings.ENV == 'development': 
            return run_evaluation_as_another_process()
        else:
            try: 
                return run_evaluation_as_another_process()
            except queue.Empty as qe:
                return EvaluationData('error', 'Took too long')
            except Exception as e:
                return EvaluationData('error', 'Unknown error')
    