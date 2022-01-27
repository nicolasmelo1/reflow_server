from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import DATETIME_TYPE
from reflow_server.formula.utils.helpers import DatetimeHelper

from datetime import datetime
import pytz
import re


class Datetime(Object):
    def __init__(self, settings):
        super().__init__(DATETIME_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def _initialize_(self, year=2000, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, timezone=None):
        """
        The Datetime object is a first class object in flow. We treat datetime as first citzens in flow so dates are like
        strings, integers, modules and others. In python dates are just a library, in flow dates can be created like

        >>> ~D[2020-4-05 11:10]
        
        Hour and minute format is optional so you can write dates with or without the hours, minutes, or seconds.
        Notice that in the example above we are surpassing the seconds, so it'll be considered as 11:10:00

        But we could as well write:
        >>> ~D[2020-4-05 11:10:50] 

        which would also be valid.
        Or just:
        >>> ~D[2020-4-05] 
        
        This becomes extremely powerful and easy for the user to write dates in flow.

        Why this is a first class citzen you might ask. Because of the tight integration with Reflow as hole. Reflow has the date field
        so when we convert it to flow we want it to act as datetime object, a datetime object needs to be something you pass through like
        variables, and you don't have to initialize a library for that. 

        On python however we would need to first import datetime and then create a new datetime object and then we would be able to use it.
        This is not newbie friendly at all, specially for something that need to be easy for users to use and make stuff with. For a productivity
        app that will probably make a have use of dates, this is not acceptable.

        Last but not least, datetime here IS NOT naive, all of them holds information about the timezone of the user, this is something we
        keep in the database and adds to the Settings object when evaluating the formula. This way we can work with datetimes more safely. Since this is all
        done automatically inside of reflow the user doesn't need to be aware with all of the problems regarding timezones.

        The timezone exists in the 'Settings' object but you can pass it when creating new instances when needed. We default the timezone to GMT.

        Args:
            year (int, optional): The year of the new date. Defaults to 2000.
            month (int, optional): The month of the new date. Defaults to 1.
            day (int, optional): The day of the new date. Defaults to 1.
            hour (int, optional): If you are creating a new datetime object with time, at least the hour needs to be configured. Defaults to 0.
            minute (int, optional): The minute of the new date, completely optional. Defaults to 0.
            second (int, optional): The second of the new date, completely optional. Defaults to 0.
            microsecond (int, optional): The microsecond of the new date, completely optional. Defaults to 0.
            timezone (str, optional): Check pytz documentation for a list of timezones, this is completely optional, you will not use it unless
                                      the user explicitly wants to create a new date with a specific timezone. Defaults to None.
        """
        self.timezone = timezone if timezone != None else self.settings.timezone

        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _equals_(self, obj):
        """
        When it equals what we do is compare if each part of the Datetime is equal to one another.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.Boolean): Returns a new boolean object

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the equals conditional. 
        """
        if obj.type == DATETIME_TYPE:
            is_datetime_objects_equal = obj.year == self.year and \
                                        obj.month == self.month and \
                                        obj.day == self.day and \
                                        obj.hour == self.hour and \
                                        obj.minute == self.minute and \
                                        obj.second == self.second and \
                                        obj.microsecond == self.microsecond 
            return super().new_boolean(is_datetime_objects_equal)
        else:
            return super()._equals_(obj)
    # ------------------------------------------------------------------------------------------
    def _difference_(self, obj):
        """
        Retrieves if two datetime objects are different from each other, if it is we return a new boolean object indicating
        that it is different, otherwise we tell it it is the same. This just works when comparing 2 datatimes.

        Args:
            obj (any): Any Flow object type is accepted but it only works if the object is a Datetime object.

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the difference conditional. 
        """
        if obj.type == DATETIME_TYPE:
            is_datetime_objects_different = obj.year != self.year or \
                                            obj.month != self.month or \
                                            obj.day != self.day or \
                                            obj.hour != self.hour or \
                                            obj.minute != self.minute or \
                                            obj.second != self.second or \
                                            obj.microsecond != self.microsecond 
            return super().new_boolean(is_datetime_objects_different)
        else:
            return super()._difference_(obj)
    # ------------------------------------------------------------------------------------------
    def _lessthan_(self, obj):
        """
        When it is less than what we do is compare if each part of the Datetime is less than to one another.

        Args:
            obj (any): Any Flow object type is accepted but it only works if the object is a Datetime object.

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the equals conditional. 
        """
        if obj.type == DATETIME_TYPE:
            representation = self._representation_()
            object_representation = obj._representation_()
            return super().new_boolean(representation < object_representation)
        else:
            return super()._lessthan_(obj)
    # ------------------------------------------------------------------------------------------
    def _lessthanequal_(self, obj):
        """
        When it is less than equal what we do is convert to a python datetime object and use this for comparison since it's a lot easier

        Args:
            obj (reflow_server.formula.utils.builtins.objects.Boolean): Returns a new boolean object

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the equals conditional. 
        """
        if obj.type == DATETIME_TYPE:
            representation = self._representation_()
            object_representation = obj._representation_()

            return super().new_boolean(representation <= object_representation)
        else:
            return super()._lessthan_(obj)
    # ------------------------------------------------------------------------------------------
    def _greaterthan_(self, obj):
        """
        When it is greater than what we do is convert to a python datetime object and use this for comparison since it's a lot easier to manage.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.Boolean): Returns a new boolean object

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the equals conditional. 
        """
        if obj.type == DATETIME_TYPE:
            representation = self._representation_()
            object_representation = obj._representation_()

            return super().new_boolean(representation > object_representation)
        else:
            return super()._lessthan_(obj)
    # ------------------------------------------------------------------------------------------
    def _greaterthanequal_(self, obj):
        """
        For comparisons like greater than equal we use the actual python datetime module to handle that this way we do not have to.

        Args:
            obj (reflow_server.formula.utils.builtins.objects.*): Any type of object can be recieved

        Returns:
            reflow_server.formula.utils.builtins.objects.Boolean.Boolean: Returns a boolean object representing either True or 
                                                                          False for the equals conditional. 
        """
        if obj.type == DATETIME_TYPE:
            representation = self._representation_()
            object_representation = obj._representation_()

            return super().new_boolean(representation >= object_representation)
        else:
            return super()._lessthan_(obj)
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        return datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            microsecond=self.microsecond,
            tzinfo=pytz.timezone(self.timezone)
        )
    # ------------------------------------------------------------------------------------------
    def _string_(self, **kwargs):
        representation = self._representation_()
        datetime_helpers = DatetimeHelper()

        datetime_helpers.append_values_by_definition('year', representation.year)
        datetime_helpers.append_values_by_definition('month', representation.month)
        datetime_helpers.append_values_by_definition('day', representation.day)
        datetime_helpers.append_values_by_definition('hour', representation.hour)
        datetime_helpers.append_values_by_definition('minute', representation.minute)
        datetime_helpers.append_values_by_definition('second', representation.second)
        datetime_helpers.append_values_by_definition('microsecond', representation.microsecond)

        date_part_of_representation = self.settings.datetime_date_format
        time_part_of_representation = self.settings.datetime_time_format

        regex_of_date_format = self.settings.date_format_to_regex(True)
        matched_date_format = re.findall(regex_of_date_format, self.settings.datetime_date_format)
        matched_date_format = matched_date_format[0] if len(matched_date_format) > 0 else []
        for format_string in matched_date_format:
            value = datetime_helpers.get_value_stringfied_by_format(format_string)
            if value != None:
                date_part_of_representation = date_part_of_representation.replace(format_string, value)
        
        regex_of_time_format = self.settings.time_format_to_regex(True)
        matched_time_format = re.findall(regex_of_time_format, self.settings.datetime_time_format)
        matched_time_format = matched_time_format[0] if len(matched_time_format) > 0 else []
        
        for format_string in matched_time_format:
            value = datetime_helpers.get_value_stringfied_by_format(format_string)
            if value != None:
                time_part_of_representation = time_part_of_representation.replace(format_string, value)
        
        return self.new_string(
            f"{self.settings.sigil_string}{self.settings.datetime_date_character}" + \
            f"[{date_part_of_representation} {time_part_of_representation}]"
        )
    # ------------------------------------------------------------------------------------------
    def _safe_representation_(self):
        return datetime(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            microsecond=self.microsecond,
            tzinfo=pytz.timezone(self.timezone)
        )