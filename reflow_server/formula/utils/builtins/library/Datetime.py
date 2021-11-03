from reflow_server.formula.utils.builtins.library.LibraryModule import LibraryModule, functionmethod, \
    retrieve_representation
from reflow_server.formula.utils.builtins import objects as flow_objects

from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import pytz


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
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(date.year)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a date')

    @functionmethod
    def month(date, **kwargs):
        if isinstance(date, flow_objects.Datetime):
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(date.month)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a datetime value')

    @functionmethod
    def day(date, **kwargs):
        if isinstance(date, flow_objects.Datetime):
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(date.day)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a datetime value')

    @functionmethod
    def hour(date, **kwargs):
        if isinstance(date, flow_objects.Datetime):
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(date.hour)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a datetime value')

    @functionmethod
    def minute(date, **kwargs):
        if isinstance(date, flow_objects.Datetime):
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(date.minute)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a datetime value')

    @functionmethod
    def second(date, **kwargs):
        if isinstance(date, flow_objects.Datetime):
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(date.second)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a datetime value')

    @functionmethod
    def microsecond(date, **kwargs):
        if isinstance(date, flow_objects.Datetime):
            return flow_objects.Integer(kwargs['__settings__'])._initialize_(date.microsecond)
        else:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'Invalid date, should be a datetime value')

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
    def date_add(value, years=0, months=0, days=0, hours=0, minutes=0, seconds=0, microseconds=0, **kwargs):
        is_valid_values = (years == 0 or isinstance(years, flow_objects.Integer) or isinstance(years, flow_objects.Float)) and \
                          (months == 0 or isinstance(months, flow_objects.Integer) or isinstance(months, flow_objects.Float)) and \
                          (days == 0 or isinstance(days, flow_objects.Integer) or isinstance(days, flow_objects.Float)) and \
                          (hours == 0 or isinstance(hours, flow_objects.Integer) or isinstance(hours, flow_objects.Float)) and \
                          (minutes == 0 or isinstance(minutes, flow_objects.Integer) or isinstance(minutes, flow_objects.Float)) and \
                          (seconds == 0 or isinstance(seconds, flow_objects.Integer) or isinstance(seconds, flow_objects.Float)) and \
                          (microseconds == 0 or isinstance(microseconds, flow_objects.Integer) or isinstance(microseconds, flow_objects.Float)) and \
                          isinstance(value, flow_objects.Datetime)
        if years == None and months == None and days == None and minutes == None and seconds == None and microseconds == None:
            flow_objects.Error(kwargs['__settings__'])._initialize_('Error', 'You should define at least one parameter to add to the date')

        elif is_valid_values:
            years = int(retrieve_representation(years))
            months = int(retrieve_representation(months))
            days = int(retrieve_representation(days))
            hours = int(retrieve_representation(hours))
            minutes = int(retrieve_representation(minutes))
            seconds = int(retrieve_representation(seconds))
            microseconds = int(retrieve_representation(microseconds))

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
    
    @functionmethod
    def difference(bigger_date, smaller_date, year=False, month=False, day=False, hour=False, minute=False, second=False, **kwargs):
        if isinstance(bigger_date, flow_objects.Datetime) and isinstance(smaller_date, flow_objects.Datetime):
            bigger_date = retrieve_representation(bigger_date)
            smaller_date = retrieve_representation(smaller_date)
            delta = relativedelta(bigger_date, smaller_date)
            result = bigger_date - smaller_date

            if isinstance(year, flow_objects.Object.Object) and year._boolean_()._representation_():
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(delta.years)
            elif isinstance(month, flow_objects.Object.Object) and month._boolean_()._representation_():
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(delta.months + (delta.years)*12)
            elif isinstance(day, flow_objects.Object.Object) and day._boolean_()._representation_():
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(result / timedelta(days=1))
            elif isinstance(hour, flow_objects.Object.Object) and hour._boolean_()._representation_():
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(result / timedelta(hours=1))
            elif isinstance(minute, flow_objects.Object.Object) and minute._boolean_()._representation_():
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(result / timedelta(minutes=1))
            elif isinstance(second, flow_objects.Object.Object) and second._boolean_()._representation_():
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(result / timedelta(seconds=1))
            else:
                return flow_objects.Integer(kwargs['__settings__'])._initialize_(result / timedelta(microseconds=1))
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
                'month': {
                    'description': 'Retrieve the month of a date. Example:\n'
                                   '>>> Datetime.year(~D[2020-10-12]) == 10',
                    'attributes': {
                        'date': {
                            'description': 'The actual date to extract the month from.',
                            'is_required': True
                        }
                    }
                },
                'day': {
                    'description': 'Retrieve the day of a date. Example:\n'
                                   '>>> Datetime.year(~D[2020-10-12]) == 12',
                    'attributes': {
                        'date': {
                            'description': 'The actual date to extract the day from.',
                            'is_required': True
                        }
                    }
                },
                'hour': {
                    'description': 'Retrieve the hour of a date. Example:\n'
                                   '>>> Datetime.year(~D[2020-10-12 20:11:40]) == 20',
                    'attributes': {
                        'date': {
                            'description': 'The actual date to extract the hour from.',
                            'is_required': True
                        }
                    }
                },
                'minute': {
                    'description': 'Retrieve the minute of a date. Example:\n'
                                   '>>> Datetime.year(~D[2020-10-12 20:11:40]) == 11',
                    'attributes': {
                        'date': {
                            'description': 'The actual date to extract the minute from.',
                            'is_required': True
                        }
                    }
                },
                'second': {
                    'description': 'Retrieve the second of a date. Example:\n'
                                   '>>> Datetime.year(~D[2020-10-12 20:11:40]) == 40',
                    'attributes': {
                        'date': {
                            'description': 'The actual date to extract the second from.',
                            'is_required': True
                        }
                    }
                },
                'microsecond': {
                    'description': 'Retrieve the microsecond of a date.',
                    'attributes': {
                        'date': {
                            'description': 'The actual date to extract the microsecond from.',
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
                },
                'difference': {
                    'description': "Retrieve the difference from two dates. This will always retrieve the difference in microseconds "
                                   "but you can extract by other dimensions like year, days or so. Example: \n"
                                   "Datetime.difference(~D[2021-11-11, ~D[2020-10-10]) == 86400000000000 \n"
                                   "Datetime.difference(~D[2021-11-11, ~D[2020-10-10], month=True) == 13",
                    'attributes': {
                        'bigger_date': {
                            'description': 'The bigger date you want to compare.',
                            'is_required': True
                        },
                        'smaller_date': {
                            'description': 'The smaller date you want to compare.',
                            'is_required': True
                        },
                        'year': {
                            'description': 'If you want to retrieve the difference in years. Defaults to False.',
                            'is_required': False
                        },
                        'month': {
                            'description': 'If you want to retrieve the difference in months. Defaults to False.',
                            'is_required': False
                        },
                        'day': {
                            'description': 'If you want to retrieve the difference in days. Defaults to False.',
                            'is_required': False
                        },
                        'hour': {
                            'description': 'If you want to retrieve the difference in hours. Defaults to False.',
                            'is_required': False
                        },
                        'minute': {
                            'description': 'If you want to retrieve the difference in minutes. Defaults to False.',
                            'is_required': False
                        },
                        'second': {
                            'description': 'If you want to retrieve the difference in seconds. Defaults to False.',
                            'is_required': False
                        }
                    }
                }
            }
        }