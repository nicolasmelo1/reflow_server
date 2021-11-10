from rest_framework import serializers

from reflow_server.analytics.models import Survey, SurveyAnswer
from reflow_server.analytics.relations import SurveyQuestionRelation, SurveyQuestionAnswerRelation
from reflow_server.analytics.services.survey import SurveyAnswerData, SurveyService

class SurveySerializer(serializers.ModelSerializer):
    survey_questions = SurveyQuestionRelation(many=True)

    class Meta:
        exclude = ('criteria_function_name', 'time_in_minutes_for_retaking', 'is_active')
        model = Survey


class SurveyAnswerSerializer(serializers.ModelSerializer):
    survey_question_answers = SurveyQuestionAnswerRelation(many=True)

    def save(self, survey_id, user_id):
        survey_service = SurveyService(user_id)
        survey_answer_data = SurveyAnswerData(survey_id)
        for survey_question_answer in self.validated_data['survey_question_answers']:
            survey_answer_data.add_question_answer(
                survey_question_answer['question_id'],
                survey_question_answer['value']
            )
        survey_service.save_survey_answer(survey_answer_data)


    class Meta:
        model = SurveyAnswer
        fields = ('survey_question_answers',)