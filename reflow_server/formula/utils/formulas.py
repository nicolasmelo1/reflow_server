from reflow_server.formula.utils.settings import Formula

import functools
import numpy as np


class FormulaSum(Formula):
    """
    This is a class for SUM formula, when you use SUM in a formula, this class is used,
    first we validate, and then we calculate. You can understand by this formula how
    formulas are handled. So it just sum the parameters
    """
    def validate(self, parameters):
        return all([type(parameter) in [int, float] for parameter in parameters])

    def calculate(self, parameters):
        """
        Calculates the SUM parameters, parameters are just a list, so we just sum a list.

        Arguments:
            parameters {list(int/float)} -- Just a list of parameters

        Returns:
            int/float -- It recieves an list of intergers and return an interger
        """
        result = 0
        if len(parameters) > 0:
            parameters = np.asarray(parameters)
            result = functools.reduce(lambda x, y: x+y, parameters)
        return result


class FormulaCount(Formula):
    """
    This is a class for COUNT formula, when you use COUNT in a formula, this class is used.
    The validate method here is not nedded since COUNT is just the length of the list
    """
    def calculate(self, parameters):
        """
        Calculates the length of the parameters, nothing much, really.

        Arguments:
            parameters {list(any)} -- Just a list of parameters

        Returns:
            int -- returns the length of the list parameters
        """
        return int(len(parameters))


class FormulaAvarege(Formula):
    """
    This class is used for AVEREGE formula. When you use AVEREGE in a formula, this class is used.
    """
    def validate(self, parameters):
        return all([type(parameter) in [int, float] for parameter in parameters])

    def calculate(self, parameters):
        """
        Calculates the averege of all of the parameters, averege is the sum divided 
        by the number of values

        Arguments:
            parameters {list(int/float)} -- Just a list of parameters

        Returns:
            int/float -- It recieves an list of numbers and return a number
        """
        result = 0
        if len(parameters) > 0:
            parameters = np.asarray(parameters)
            result = functools.reduce(lambda x, y: x+y, parameters)
            result = result/len(parameters)
        return int(result)
