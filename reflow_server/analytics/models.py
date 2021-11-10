from django.db import models

from reflow_server.analytics.managers import TypeOfEventAnalyticsManager, EventAnalyticsManager, \
    SurveyAnalyticsManager, SurveyAnswerAnalyticsManager, SurveyQuestionAnswerAnalyticsManager
from reflow_server.authentication.managers import CompanyAnalyticsAuthenticationManager


class Survey(models.Model):
    """
    In order to make better analytics and focus our product better as the user want, we need to know stuff from the user.
    This stuff is something we cannot take from third party apps like Google Analytics or Mixpanel, we also cannot
    extract from our data.

    Questions like the NPS score, "How would you feel if you could no longer use reflow?" and so on.
    So this was created to solve this problem and give us the data we need to understand more about our users behaviour.

    We have 2 special columns here:
    `criteria_function_name` - Will be the function to run to validate if the criteria for the survey matches. (we might
    want to create a survey only for males for example, or we might want to create a survey only for admins).
    Because we want those functions to be reused we created the `SurveyCriteriaData` model that will give use the parameters
    of the function.
    `time_in_seconds_for_retaking` - Some of them might be retaken after some time, so we need to know how much time we need 
    to await before showing the user the survey again.
    `is_active` - is the survey active or not.
    """
    survey_name = models.TextField()
    does_display_survey_name = models.BooleanField(default=False)
    criteria_function_name = models.CharField(max_length=255, null=True, blank=True)
    time_in_minutes_for_retaking = models.BigIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'survey'

    objects = models.Manager()
    analytics_ = SurveyAnalyticsManager()

class SurveyCriteriaData(models.Model):
    """
    Explained above in the Survey model. But anyway, since we want our criteria functions to be as reusable as possible.
    We created this model to store the data that will be used as attributes for the function. The key will be the name of the parameter
    and the value is the value of the parameter.

    This doesn't need to be set, you can have just fuctions that doesn't recieve any argument.
    """
    survey = models.ForeignKey('analytics.Survey', on_delete=models.CASCADE, related_name='survey_criteria_data')
    key = models.CharField(max_length=255)
    value = models.TextField()

    class Meta:
        db_table = 'survey_criteria_data'


class SurveyQuestion(models.Model):
    """
    This is each Question of the survey. To make it simple, the questions will be text by default. But if we define options
    using SurveyQuestionOption model then we will display the options to the user for him to select. Similar to formularies, questions
    can be required or not. Really simple stuff.
    """
    survey = models.ForeignKey('analytics.Survey', on_delete=models.CASCADE, related_name='survey_questions')
    is_required = models.BooleanField(default=True)
    question = models.TextField()

    class Meta:
        db_table = 'survey_question'


class SurveyQuestionOption(models.Model):
    """
    Explained above, but this will hold each option for a given question. Really simple stuff.

    although the options are simple we can have special options like 'likert'. Likert scale are represented like:
    "On a rate from 1 to 10, how much do you like this?"

    And show a scale in the horizontal. Because of that we have the special `range_value` this represents what value does it represent from the scale.

    The likert scale always starts from 1, and can go for whatever number you want.
    """
    question = models.ForeignKey('analytics.SurveyQuestion', on_delete=models.CASCADE, related_name='survey_question_options')
    option = models.TextField()
    range_value = models.IntegerField(null=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'survey_question_option'
        ordering = ('order',)


class SurveyAnswer(models.Model):
    """
    The answer recieved from the user.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey('analytics.Survey', on_delete=models.CASCADE, related_name='survey_answers', null=True)
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, related_name='survey_answer_users')

    class Meta:
        db_table = 'survey_answer'

    analytics_ = SurveyAnswerAnalyticsManager()


class SurveyQuestionAnswer(models.Model):
    """
    Answer but each value from each question that the user sent.
    """
    question = models.ForeignKey('analytics.SurveyQuestion', on_delete=models.CASCADE, related_name='survey_question_answer_questions')
    answer = models.ForeignKey('analytics.SurveyAnswer', on_delete=models.CASCADE, related_name='survey_question_answers')
    value = models.TextField()

    class Meta:
        db_table = 'survey_question_answer'

    analytics_ = SurveyQuestionAnswerAnalyticsManager()


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