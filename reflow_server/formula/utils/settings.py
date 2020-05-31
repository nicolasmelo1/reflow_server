from reflow_server.formula.models import FormulaType

import string
import random

class Structure:
    operations = {
        '>=': '>=',
        '<=': '<=',
        '<>': '!=',
        '<': '<',
        '>': '>',
        '/':'/', 
        '&':'+',
        '%':'%', 
        '-':'-', 
        '+':'+',
        '*':'*',
        '^':'**', 
        '=': '=='
    }

    types = ['string', 'field', 'number', 'operation']

    formulas = {}

    to_tokenize = [
        ('string', r'"[^"]*"'),
        ('field', r'{{[^{{]*}}'),
        ('number', r'[\d_]+\.[\d]+|[\d_]+,[\d]+|[\d_]+'),
        ('operation', '|'.join(['\\' + operator for operator in operations.keys()]))
    ]

    valid_characters = [
        '(', ')', ';'
    ]
     
    def __init__(self, *args, **kwargs):
        self.formulas = FormulaType.objects.all().values_list('name', flat=True)

    def is_formula(self, token):
        return token in self.formulas

class Formula:
    def validate(self, parameters):
        return True