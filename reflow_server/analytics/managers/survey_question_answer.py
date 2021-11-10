from django.db import models


class SurveyQuestionAnswerAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create(self, answer_id, question_id, value):
        return self.get_queryset().create(
            answer_id=answer_id,
            question_id=question_id,
            value=value
        )
