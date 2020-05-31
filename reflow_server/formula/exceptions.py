from rest_framework import serializers

class FormulaException(Exception):
    pass

class ValidateError(serializers.ValidationError):
    pass