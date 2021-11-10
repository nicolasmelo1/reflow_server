from django.utils import timezone

from reflow_server.analytics.models import Survey, SurveyAnswer, SurveyQuestionAnswer

from datetime import datetime, timedelta

from reflow_server.authentication.models import UserExtended

cached_survey_ids = {
    'expiry_date': datetime.now() + timedelta(days=1),
    'surveys': []
}

class SurveyAnswerData:
    class SurveyQuestionAnswerData:
        def __init__(self, question_id, answer_value):
            self.question_id = question_id
            self.answer_value = answer_value

    def __init__(self, survey_id):
        self.survey_id = survey_id
        self.question_answers = []

    def add_question_answer(self, question_id, answer_value):
        self.question_answers.append(self.SurveyQuestionAnswerData(question_id, answer_value))


class SurveyService:
    def __init__(self, user_id):
        self.user_id = user_id
    
    def display_survey_id(self):
        """
        Function used to check if we need to display a given survey for the user or not. We check time in minutes to wait before retaking the survey.
        We check the criteria function name if it exists and last but not least we check if the survey has already been answered by the user.
        On the last one, if the survey have not been answered yet we will show it to him.

        Returns:
            survey_id: (int, None) - The id of the survey to show or None. You might ask yourself, why return just one if two or more surveys
            need to be responded? The answer is UX. We can show the other one he needs to respond to tomorrow.
        """        
        if cached_survey_ids['expiry_date'] < datetime.now() or len(cached_survey_ids['surveys']) == 0:
            cached_survey_ids['surveys'] = Survey.analytics_.active_surveys_id_time_in_minutes_for_retaking_and_criteria_function_name()
        
        surveys = cached_survey_ids['surveys']
        for survey in surveys:
            if survey['time_in_minutes_for_retaking'] != 0:
                latest_time_the_user_answered = SurveyAnswer.analytics_.latest_survey_answer_date_by_survey_id_and_user_id(survey['id'], self.user_id)
                if latest_time_the_user_answered:
                    timesince = timezone.now() - latest_time_the_user_answered
                    minutessince = int(timesince.total_seconds() / 60)

                    if minutessince > survey['time_in_minutes_for_retaking']:
                        return survey['id']

            if survey['criteria_function_name']:
                handler = hasattr(self, 'check_criteria_{}'.format(survey['criteria_function_name']))
                if handler and handler(survey['id']):
                    return survey['id']

            did_the_user_answer = SurveyAnswer.analytics_.exists_survey_answer_by_survey_id_and_user_id(survey['id'], self.user_id)
            has_user_created_account_in_the_last_30_days = UserExtended.analytics_.has_user_joined_reflow_from_at_least_30_days(self.user_id)
            if not did_the_user_answer and has_user_created_account_in_the_last_30_days:
                return survey['id']
        
        return None

    def save_survey_answer(self, survey_answer_data):
        """
        Function used to save the answer of a survey.
        """

        survey_answer = SurveyAnswer.analytics_.create(
            survey_id=survey_answer_data.survey_id,
            user_id=self.user_id
        )

        for question_answer in survey_answer_data.question_answers:
            SurveyQuestionAnswer.analytics_.create(
                answer_id=survey_answer.id,
                question_id=question_answer.question_id,
                value=question_answer.answer_value
            )

        
        