from django.conf import settings

from reflow_server.data.models import FormValue
from reflow_server.formulary.models import FormulaVariable, FieldType, FieldNumberFormatType
from reflow_server.formula.utils import evaluate
from reflow_server.formula.utils.context import Context
from reflow_server.formula.models import FormulaContextForCompany, FormulaContextAttributeType

import queue
import multiprocessing
import json
import base64
import re


class FormulaVariables:
    def __init__(self):
        self.variables = []
    
    def add_variable_id(self, variable_id):
        self.variables.append(variable_id)


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
        

class FormulaService:
    def __init__(self, formula, company_id, dynamic_form_id=None, field_id=None, formula_variables=None):
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
        """
        if formula_variables == None:
            formula_variables = FormulaVariables()
            variable_ids = FormulaVariable.formula_.variable_ids_by_field_id(field_id)
            for variable_id in variable_ids:
                formula_variables.add_variable_id(variable_id)

        self.__build_context(company_id)
        self.formula = self.__clean_formula(formula, dynamic_form_id, formula_variables)

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
        for index, variable_id in enumerate(formula_variables.variables):
            values = FormValue.formula_.values_and_field_type_by_main_formulary_data_id_and_field_id(
                dynamic_form_id,
                variable_id
            )
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
                'value': evaluate(formula, self.context)
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

