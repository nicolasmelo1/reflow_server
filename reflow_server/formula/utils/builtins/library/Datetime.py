from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

from dateutil.relativedelta import relativedelta


class Datetime(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self

    @functionmethod
    def date_add(self, value, years=None, months=None, days=None, hours=None, minutes=None, seconds=None, microseconds=None, **kwargs):
        is_valid_values = (years == None or isinstance(years, flow_objects.Integer) or isinstance(years, int)) and \
                          (months == None or isinstance(months, flow_objects.Integer) or isinstance(months, int)) and \
                          (days == None or isinstance(days, flow_objects.Integer) or isinstance(days, int)) and \
                          (hours == None or isinstance(hours, flow_objects.Integer) or isinstance(hours, int)) and \
                          (minutes == None or isinstance(minutes, flow_objects.Integer) or isinstance(minutes, int)) and \
                          (seconds == None or isinstance(seconds, flow_objects.Integer) or isinstance(seconds, int)) and \
                          (microseconds == None or isinstance(microseconds, flow_objects.Integer) or isinstance(microseconds, int)) and \
                          isinstance(value, flow_objects.Datetime)

        if is_valid_values:
            years = retrieve_representation(years)
            months = retrieve_representation(months)
            days = retrieve_representation(days)
            hours = retrieve_representation(hours)
            minutes = retrieve_representation(minutes)
            seconds = retrieve_representation(seconds)
            microseconds = retrieve_representation(microseconds)

            value = retrieve_representation(value)

            if years != None:
                value = value + relativedelta(years=years)
            if months != None:
                value = value + relativedelta(months=months)
            if days != None:
                value = value + relativedelta(days=days)
            if hours != None:
                value = value + relativedelta(hours=hours)
            if minutes != None:
                value = value + relativedelta(minutes=minutes)
            if seconds != None:
                value = value + relativedelta(seconds=seconds)
            if microseconds != None:
                value = value + relativedelta(microseconds=microseconds)
            
            result = flow_objects.Datetime(kwargs['__settings__'])
            return result._initialize_(value.year, value.month, value.day, value.hour, value.minute, value.second, value.microsecond)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid value for function')
    
    def _documentation_(self):
        """
        This is the documentation of the formula, this is required because even if we do not translate the formula documentation directly, we need to have
        any default value so users can know what to do and translators can understand how to translate the formula.
        """
        return {
            "description": "Module responsible for doing stuff with datetime, this is responsible for things like adding dates, getting the current "
                           "date and so on.",
            "methods": {
                "date_add": {
                    'description': 'Adds or subtracts years, months, days, hours, minutes, seconds or microseconds to a date',
                    'attributes': {
                        'value': {
                            'description': 'The datetime value you are adding or subtracting, you need to pass it here.',
                            'is_required': True
                        }, 
                        'years': {
                            'description': 'Number of years you want to add or subtract. Default as None.',
                            'is_required': False
                        }, 
                        'months': {
                            'description': 'Number of months you want to add or subtract. Defaults to None.',
                            'is_required': False
                        },
                        'days': {
                            'description': 'Number of days you want to add or subtract. Defaults to None.',
                            'is_required': False
                        },
                        'hours': {
                            'description': 'Number of hours you want to add or subtract. Defaults to None.',
                            'is_required': False
                        },
                        'minutes': {
                            'description': 'Number of minutes you want to add or subtract. Defaults to None.',
                            'is_required': False
                        },
                        'seconds': {
                            'description': 'Number of seconds you want to add or subtract. Defaults to None.',
                            'is_required': False
                        },
                        'microseconds': {
                            'description': 'Number of microseconds you want to add or subtract. Defaults to None.',
                            'is_required': False
                        }
                    }
                }
            }
        }