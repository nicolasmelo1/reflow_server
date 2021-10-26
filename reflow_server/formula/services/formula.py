from django.conf import settings
from django import db

from reflow_server.data.models import FormValue
from reflow_server.data.services.representation import RepresentationService
from reflow_server.formulary.models import FieldDateFormatType, FormulaVariable, FieldType, FieldNumberFormatType
from reflow_server.formula.services.data import FormulaVariables, EvaluationData, InternalValue
from reflow_server.formula.utils import evaluate
from reflow_server.formula.utils.helpers import DatetimeHelper
from reflow_server.formula.services.utils import build_context
from reflow_server.formula.models import FormulaContextForCompany, FormulaContextType
from reflow_server.authentication.models import UserExtended 

from datetime import datetime
import logging
import queue
import multiprocessing
import re


class FlowFormulaService:
    def __init__(self, formula, user_id, company_id, dynamic_form_id=None, field_id=None, formula_variables=None, is_testing=False):
        """
        This service is handy for interacting with formulas in reflow, this service holds all of the logic needed to run our programming
        language. This is the interface you generally will use for interacting with formulas. Simple as that.

        Why do we need an interface?

        That's simple, when you want to run stuff like 

            status = {{status_553}}
            if status == "Fechado" do
                "O status está Fechado"
            end 

        our formula doesn't understand {{status_553}} this does not mean anything to it. This is a variable that we enable users to type
        and use values of a field inside of a formula. Understandable, so how we do it.

        We do it by getting the variable actual value and transforming it to a value the programming language actually understands.

        So the example above becomes:

            status = "Perdido"
            if status == "Fechado" do
                "O status está Fechado"
            end

        and we can then evaluate the formula.

        The same happens the other way around. We evaluated the formula and the Formula gave us a reflow_server.formula.utils.builtin.objects.Integer.Integer
        object. This doesn't mean anything to reflow itself, so we then need to transform it to a valua reflow is actually able to understand
        and comprehend. (we use it with '.to_internal_value()' function)

        Nice? Yeah it is.

        Args:
            formula (str): The actual formula string to clean and evaluate.
            company_id (int): A Company instance id
            dynamic_form_id (int, optional): A DynamicForm instance id. THIS IS A MAIN FORM INSTANCE ID, with depends_on as None. Defaults to None.
            field_id (int, optional): The formula is usually bounded to a field, this is the field id the formula is bounded to. Defaults to None.
            formula_variables (reflow_server.formula.services.FormulaVariables, optional): A FormulaVariables object that has a list of all variable_ids, each variable_id is a Field
                                                                                           instance id. Defaults to None.
            is_testing(bool, optional): If you are testing out the formula then the clean process will create dummy values if nothing is found.
        """
        user_timezone = UserExtended.formula_.timezone_by_user_id(user_id)
        if formula_variables == None:
            formula_variables = FormulaVariables()
            variable_ids = FormulaVariable.formula_.variable_ids_by_field_id(field_id)
            for variable_id in variable_ids:
                if isinstance(variable_id, int) or variable_id.isdigit():
                    formula_variables.add_variable_id(variable_id)

        context_type_id = FormulaContextForCompany.formula_.formula_context_for_company_by_company_id(company_id)
        self.is_testing = is_testing
        self.context = build_context(context_type_id, 'formula')
        self.context.add_reflow_data(company_id, user_id, dynamic_form_id=dynamic_form_id)
        
        self.context.datetime.timezone = user_timezone
        
        self.formula = self.__clean_formula(formula, dynamic_form_id, formula_variables)
    # ------------------------------------------------------------------------------------------
    def __clean_formula(self, formula, dynamic_form_id, formula_variables):
        """
        This cleans the formula, what is cleaning the formula you might ask yourself.

        Cleaning the formula is the process of getting the {{variable}} and adding a real value
        that the formulas can understand to it.

        For example:
            
            status = {{status_553}}
            if status == "Fechado" do
                "O status está Fechado"
            end

        The formula by itself cannot understand {{status_553}}, so we need to transform it to a REAL value the formula can understand.
        In other words, to a String, to a Float, to a Integer, and so on.

        So let's suppose we are saving the formulary with the following data:
        {
            "id": null,
            "uuid": "9e853e6a-1315-4bbf-a3db-33f9e4b9d3f0",
            "depends_on_dynamic_form": [
                {
                    "id": null,
                    "uuid": "b1e89bfa-88a2-41e8-9ea0-c8fbda1f0bd8",
                    "form_id": 334,
                    "dynamic_form_value": {
                        "id": null,
                        "field_id": 553,
                        "field_name": "status_553",
                        "value": "Perdido"
                    }
                }
            ]
        }

        What do we do on the formula is this:
            
            status = "Perdido"
            if status == "Fechado" do
                "O status está Fechado"
            end

        Did you notice? We've changed {{status_555}} with the "Perdido" string.
        
        Args:
            formula (str): The unformatted formula, with the variable tags ( {{}} )
            dynamic_form_id (int): A reflow_server.data.models.DynamicForm instance id WITH depends_on as NULL
            field_id (int): The field instance id of the formula.

        Returns:
            str: Returns the formatted and cleaned formula.
        """
        variables = re.findall(r'{{\w*?}}', formula, re.IGNORECASE)
        for index, formula_variable in enumerate(formula_variables.variables):
            values = FormValue.formula_.values_and_field_type_by_main_formulary_data_id_and_field_id(
                dynamic_form_id,
                formula_variable.variable_id
            )
            if len(values) == 1:
                handler = getattr(self, '_clean_formula_%s' % formula_variable.field_type, None)
                # if there is no handler for the field type, consider it as a string by default
                # if you have a handler you can bypass the representation of the data
                representation = RepresentationService(
                    field_type=formula_variable.field_type,
                    date_format_type_id=formula_variable.date_format_id,
                    number_format_type_id=formula_variable.number_format_id,
                    form_field_as_option_id=formula_variable.form_field_as_option_id
                )
                if handler:
                    value_to_replace = handler(representation, values[0]['value'])
                else:
                    value = representation.representation(values[0]['value'])
                    value_to_replace = '"{}"'.format(value)
            else:
                handler = getattr(self, '_clean_formula_%s' % formula_variable.field_type, None)
                if handler:
                    value_to_replace = handler(None, None)
                else:
                    value_to_replace = '""'
            formula = formula.replace(variables[index], value_to_replace, 1)
        return formula
    # ------------------------------------------------------------------------------------------
    def _clean_formula_number(self, representation, value):
        """
        Looks kinda dumb, but the idea is simple, we transform it to a representation, and then we 
        strip everything that is not a number or a decimal separator from the number. (
            We can have numbers like 200,00 % or 2.000.000,50 so what we do is strip the thousand separator, along with prefix
            and suffixes of the number.
        )

        Then this might not be clear. We change the decimal separator for '.' so in the example above '200,00 %' becomes '200.0' and then
        we transform it to a base. (what?) 200,00 % should be considered as 2.0 don't you think? And 50% should be considered as 0.5, so what we do
        is divide by the base and then transform it again to string changing the decimal_separator with the CONTEXT decimal separator.

        Args:
            representation (reflow_server.data.services.representation.RepresentationService, None): The representationService object for the field
            value (str, None): The actual value to subtitute for

        Returns:
            str: The new value to substitute the variable for
        """
        if representation != None and value != None:
            value = representation.representation(value)
            value = value if value not in ['', None] else '1'

            decimal_separator = representation.number_format_type.decimal_separator
            decimal_separator = decimal_separator if decimal_separator else ''
            # split the values and get only decimal separator and numbers (prefix and suffix are removed)
            splitted_value = list(value)
            splitted_value = [character for character in splitted_value if character.isdigit() or character == decimal_separator]
            # decimal separator is replaced to '.' so we can transform to float.
            # we should consider 20,0% as 0,20 don't you think? So that's why we do this. and then we convert back to string
            if (decimal_separator != '' and decimal_separator in splitted_value):
                actual_number = ''.join(splitted_value).replace(
                    decimal_separator, 
                    '.'
                )
            else:
                actual_number = ''.join(splitted_value)

            actual_number = str(float(actual_number)/representation.number_format_type.base)
            actual_number = actual_number.replace('.', self.context.decimal_point_separator)
        else:
            value = '1'
        return actual_number
    # ------------------------------------------------------------------------------------------
    def _clean_formula_date(self, representation, value):
        if representation != None and value != None:
            if value in ['', None] and self.is_testing:
                python_datetime_value = datetime.now()
            else:
                python_datetime_value = datetime.strptime(value, settings.DEFAULT_DATE_FIELD_FORMAT)

            flow_formated_datetime = python_datetime_value.strftime(DatetimeHelper.to_python_format(self.context.datetime.date_format, self.context.datetime.time_format))
            return f'~{self.context.datetime.date_character}[{flow_formated_datetime}]'
        else:
            return '""'
    # ------------------------------------------------------------------------------------------
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
    # ------------------------------------------------------------------------------------------
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
            value_type = formula_result.value.type if formula_result.value else ''
            handler = getattr(self, '_to_internal_value_%s' % value_type, None)
            if handler:
                return handler(formula_result)               
        elif formula_result.status == 'error':
            return InternalValue('-' if formula_result.value == 'Unknown' else '-', field_type=default_field_type)
    
        return InternalValue('-', default_field_type)
    # ------------------------------------------------------------------------------------------
    def _to_internal_value_datetime(self, formula_result):
        field_type = FieldType.objects.filter(type='date').first()
        date_format_type = FieldDateFormatType.objects.filter(type='datetime').first()
        value = formula_result.value._representation_().strftime(settings.DEFAULT_DATE_FIELD_FORMAT)

        return InternalValue(value, field_type, date_format_type=date_format_type)
    # ------------------------------------------------------------------------------------------
    def _to_internal_value_int(self, formula_result):
        field_type = FieldType.objects.filter(type='number').first()
        number_format_type = FieldNumberFormatType.objects.filter(type='number').first()
        value = formula_result.value._safe_representation_() * settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT

        return InternalValue(value, field_type, number_format_type=number_format_type)
    # ------------------------------------------------------------------------------------------
    def _to_internal_value_float(self, formula_result):
        field_type = FieldType.objects.filter(type='number').first()
        number_format_type = FieldNumberFormatType.objects.filter(type='number').first()
        splitted_value = str(formula_result.value._safe_representation_() * settings.DEFAULT_BASE_NUMBER_FIELD_FORMAT).split('.')
        value = splitted_value[0]     

        return InternalValue(value, field_type, number_format_type=number_format_type)
    # ------------------------------------------------------------------------------------------
    def _to_internal_value_string(self, formula_result):
        field_type = FieldType.objects.filter(type='text').first()
        value = formula_result.value._safe_representation_()

        return InternalValue(value, field_type)
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
            db.connection.connect()
            
            logging.error(formula)
            formula_result = evaluate(formula, self.context)
            status = 'error' if getattr(formula_result, 'type', '') == 'error' else 'ok'
            result.put({
                'status': status,
                'value': formula_result
            })
        
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
    def evaluate(self):
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
            process = multiprocessing.Process(target=self.__evaluate, args=(self.formula, result))
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
    # ------------------------------------------------------------------------------------------
    @staticmethod
    def update_company_formula_context(company):
        """
        Updates the context of the formulas for the company, is it portuguese, is it english is it arabic and so on.
        TODO: Right now e default to portuguese but for internalization purposes this might be dynamic in the future.
        """
        formula_context_type = FormulaContextType.objects.filter(name='portuguese').first()
    
        FormulaContextForCompany.objects.update_or_create(
            company=company,
            context_type=formula_context_type
        )