from django.db import models

from reflow_server.analytics.managers import TypeOfEventAnalyticsManager, EventAnalyticsManager
from reflow_server.authentication.managers import CompanyAnalyticsAuthenticationManager


class CompanyAnalytics(models.Model):
    company = models.OneToOneField('authentication.Company', on_delete=models.CASCADE, default=None)
    number_of_employees = models.IntegerField(null=True, default=0)
    sector = models.CharField(max_length=500, default=None, null=True, blank=True)

    class Meta:
        db_table = 'company_analytics'

    objects = models.Manager()
    authentication_ = CompanyAnalyticsAuthenticationManager()


class TypeOfEvent(models.Model):
    """
    This holds the event_name, the event is dynamic, we do not update directly in the database the event name
    What we do is set the event name in the `EVENTS` setting in `settings.py`.

    So what we do is: We first check if the event_name that we are recieving is saved in the 'type_of_event' table, if it's not
    it is probably a new event, so we save it.

    At the same time, if the name of an event had been changed we DO NOT TRACK THE CHANGE, so it's important to keep track of it elsewhere
    """
    event_name = models.CharField(max_length=280)

    class Meta:
        db_table = 'type_of_event'

    analytics_ = TypeOfEventAnalyticsManager()
############################################################################################
class Event(models.Model):
    """
    This is the actual event, the event works similarly to DynamicForms and FormValue tables. The Event table holds
    the id of each event while the EventData holds the actual value for each key we are tracking of the event.
    """
    type_of_event = models.ForeignKey('analytics.TypeOfEvent', on_delete=models.CASCADE, default=None)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'event'

    analytics_ = EventAnalyticsManager()
############################################################################################
class EventData(models.Model):
    event = models.ForeignKey('analytics.Event', on_delete=models.CASCADE, default=None)
    parameter_name = models.CharField(max_length=300)
    value = models.TextField()

    class Meta:
        db_table = 'event_data'
############################################################################################