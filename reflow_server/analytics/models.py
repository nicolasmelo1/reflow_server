from django.db import models


class TypeOfEvent:
    event_name = models.CharField(max_length=280)

    class Meta:
        db_table = 'type_of_event'
############################################################################################
class Event:
    type_of_event = models.ForeignKey('analytics.TypeOfEvent', on_delete=models.CASCADE, default=None)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'event'
############################################################################################
class EventData:
    event = models.ForeignKey('analytics.Event', on_delete=models.CASCADE, default=None)
    parameter_name = models.CharField(max_length=300)
    value = models.TextField()

    class Meta:
        db_table = 'event_data'
############################################################################################