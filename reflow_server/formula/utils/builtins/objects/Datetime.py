from reflow_server.formula.utils.builtins.objects.Object import Object
from reflow_server.formula.utils.builtins.types import DATETIME_TYPE
from reflow_server.formula.utils.helpers import DatetimeHelper

from datetime import datetime
import re

class Datetime(Object):
    def __init__(self, settings):
        super().__init__(DATETIME_TYPE, settings)
    # ------------------------------------------------------------------------------------------
    def get_formated(self, value, value_regex, format_regex, original_format):
        from reflow_server.formula.utils.builtins.objects.Error import Error

        matched_values = re.findall(value_regex, value)
        matched_format = re.findall(format_regex, original_format)[0]
        if len(matched_values) > 0:
            matched_values = matched_values[0]
            for index, matched_character in enumerate(matched_format):
                self.datetime_helper.append_values(matched_character, matched_values[index])
        else:
            Error(self.settings)._initialize_('Error', 'Invalid part of datetime: "{}"'.format(value))
    # ------------------------------------------------------------------------------------------
    def _initialize_(self, value, timezone=None):
        from reflow_server.formula.utils.builtins.objects.Error import Error

        self.datetime_helper = DatetimeHelper()
        self.timezone = timezone if timezone != None else self.settings.timezone
        splited_datetime_by_date_and_time = value.split(' ', 1)
        if len(splited_datetime_by_date_and_time) > 0:
            if re.search(self.settings.date_format_to_regex(), splited_datetime_by_date_and_time[0]):
                self.get_formated(
                    splited_datetime_by_date_and_time[0],
                    self.settings.date_format_to_regex(),
                    self.settings.date_format_to_regex(True),
                    self.settings.datetime_date_format
                )
                if len(splited_datetime_by_date_and_time) > 1:
                    self.get_formated(
                        splited_datetime_by_date_and_time[1],
                        self.settings.time_format_to_regex(),
                        self.settings.time_format_to_regex(True),
                        self.settings.datetime_time_format
                    )
            else:
                Error(self.settings)._initialize_('Error', 'Invalid datetime: "{}"'.format(value))
        else:
            Error(self.settings)._initialize_('Error', 'Invalid datetime: "{}"'.format(value))

        self.value = value
        return super()._initialize_()
    # ------------------------------------------------------------------------------------------
    def _representation_(self):
        return datetime(
            year=self.datetime_helper.get_value('year'),
            month=self.datetime_helper.get_value('month'),
            day=self.datetime_helper.get_value('day'),
            hour=self.datetime_helper.get_value('hour'),
            minute=self.datetime_helper.get_value('minute'),
            second=self.datetime_helper.get_value('second'),
            microsecond=self.datetime_helper.get_value('microsecond')
        )