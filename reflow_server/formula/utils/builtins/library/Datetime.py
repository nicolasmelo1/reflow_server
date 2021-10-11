import pytz
from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

from dateutil.relativedelta import relativedelta
from datetime import datetime


class Datetime(LibraryModule):
    def _initialize_(self, scope):
        super()._initialize_(scope=scope, struct_parameters=[])
        return self

    @functionmethod
    def now(**kwargs):
        settings = kwargs['__settings__']
        now = datetime.now(pytz.timezone(settings.timezone))
        return flow_objects.Datetime(kwargs['__settings__'])._initialize_(now.year, now.month, now.day, now.hour, now.minute, now.second, now.microsecond)
    
    @functionmethod
    def year(date, **kwargs):
        if isinstance(date, flow_objects.Datetime):
            date = retrieve_representation(date)
            year = date.year
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(year)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a date')

    @functionmethod
    def new_date(year, month, day, hour=0, minute=0, second=0, microsecond=0, **kwargs):
        is_valid_values = (year == None or isinstance(year, flow_objects.Integer) or isinstance(year, int)) and \
                          (month == None or isinstance(month, flow_objects.Integer) or isinstance(month, int)) and \
                          (day == None or isinstance(day, flow_objects.Integer) or isinstance(day, int)) and \
                          (hour == None or isinstance(hour, flow_objects.Integer) or isinstance(hour, int)) and \
                          (minute == None or isinstance(minute, flow_objects.Integer) or isinstance(minute, int)) and \
                          (second == None or isinstance(second, flow_objects.Integer) or isinstance(second, int)) and \
                          (microsecond == None or isinstance(microsecond, flow_objects.Integer) or isinstance(microsecond, int))
        
        if is_valid_values:
            year = retrieve_representation(year)
            month = retrieve_representation(month)
            day = retrieve_representation(day)
            hour = retrieve_representation(hour)
            minute = retrieve_representation(minute)
            second = retrieve_representation(second)
            microsecond = retrieve_representation(microsecond)

            if month > 12 or month < 1:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'month should be between 1 and 12')
            elif day > 31 or day < 1:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'day should be between 1 and 31')
            elif hour > 23 or hour < 0:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'hour should be between 0 and 23')
            elif minute > 59 or minute < 0:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'minute should be between 0 and 59')
            elif second > 59 or second < 0:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'second should be between 0 and 59')
            elif microsecond > 999 or microsecond < 0:
                flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'microsecond should be between 0 and 999')
            else:
                result = flow_objects.Datetime(kwargs['__settings__'])
                return result._initialize_(year, month, day, hour, minute, second, microsecond)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', '`year`, `month`, `day`, `hour`, `minute`, `second` or `microsecond` has wrong value')

    @functionmethod
    def date_add(value, years=None, months=None, days=None, hours=None, minutes=None, seconds=None, microseconds=None, **kwargs):
        is_valid_values = (years == None or isinstance(years, flow_objects.Integer) or isinstance(years, int)) and \
                          (months == None or isinstance(months, flow_objects.Integer) or isinstance(months, int)) and \
                          (days == None or isinstance(days, flow_objects.Integer) or isinstance(days, int)) and \
                          (hours == None or isinstance(hours, flow_objects.Integer) or isinstance(hours, int)) and \
                          (minutes == None or isinstance(minutes, flow_objects.Integer) or isinstance(minutes, int)) and \
                          (seconds == None or isinstance(seconds, flow_objects.Integer) or isinstance(seconds, int)) and \
                          (microseconds == None or isinstance(microseconds, flow_objects.Integer) or isinstance(microseconds, int)) and \
                          isinstance(value, flow_objects.Datetime)
        if years == None and months == None and days == None and minutes == None and seconds == None and microseconds == None:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'You should define at least one parameter to add to the date')

        elif is_valid_values:
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
                "now": {
                    'description': 'Get the current date and time of the user local.'
                },
                'year': {
                    'description': 'Retrieve the year of a date. Example:\n'
                                   '>>> Datetime.year(~D[2020-10-12]) == 2020',
                    'attributes': {
                        'date': {
                            'description': 'The actual date to extract the year from.',
                            'is_required': True
                        }
                    }
                },
                'new_date': {
                    'description': 'Creates a new date programatically. While you can create dates like'
                                   '`~D[2020-10-12]` you cannot create them programatically passing variables'
                                   'or result of functions. This is why new_date exists.',
                    'attributes': {
                        'year': {
                            'description': 'A number of the year of the new date.',
                            'is_required': True
                        }, 
                        'month': {
                            'description': 'A number of the month of the new date. Should be between 1 and 12.',
                            'is_required': True
                        },
                        'day': {
                            'description': 'A number of the day of the new date. Should be between 1 and 31.',
                            'is_required': True
                        },
                        'hour': {
                            'description': 'A number of the hour of the new date. Should be between 0 and 23. Defaults to 0.',
                            'is_required': False
                        },
                        'minute': {
                            'description': 'A number of the minute of the new date. Should be between 0 and 59. Defaults to 0.',
                            'is_required': False
                        },
                        'second': {
                            'description': 'A number of the second of the new date. Should be between 0 and 59. Defaults to 0.',
                            'is_required': False
                        },
                        'microsecond': {
                            'description': 'A number of the microsecond of the new date. Should be between 0 and 999. Defaults to 0.',
                            'is_required': False
                        }
                    }
                },
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