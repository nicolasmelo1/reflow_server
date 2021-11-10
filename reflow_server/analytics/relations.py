from rest_framework import serializers

from reflow_server.analytics.models import SurveyQuestion, SurveyQuestionOption, SurveyQuestionAnswer


class SureyQuestionOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = SurveyQuestionOption
        exclude = ('order',)


class SurveyQuestionRelation(serializers.ModelSerializer):
    survey_question_options = SureyQuestionOptionRelation(many=True)

    class Meta:
        model = SurveyQuestion
        fields = '__all__'


class SurveyQuestionAnswerRelation(serializers.ModelSerializer):
    question_id = serializers.IntegerField()
    value = serializers.CharField()

    class Meta:
        model = SurveyQuestionAnswer
        fields = ('question_id', 'value')