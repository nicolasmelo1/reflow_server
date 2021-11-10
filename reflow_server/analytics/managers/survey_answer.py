from django.db import models


class SurveyAnswerAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def latest_survey_answer_date_by_survey_id_and_user_id(self, survey_id, user_id):
        """
        Retrieves the latest survey answered by a given survey_id and user_id. This way we check if the user has answered the survey
        at a given date.

        Args:
            survey_id: The survey id to check if the user answered.
            user_id: The user id to check if he answered.
        
        Returns:
            (django.utils.timezone, None): The latest survey date answered by the user.
        """
        try:
            return self.get_queryset().filter(survey_id=survey_id, user_id=user_id).values_list('created_at', flat=True).latest('created_at')
        except:
            return None

    def exists_survey_answer_by_survey_id_and_user_id(self, survey_id, user_id):
        return self.get_queryset().filter(survey_id=survey_id, user_id=user_id).exists()

    def create(self, survey_id, user_id):
        return self.get_queryset().create(survey_id=survey_id, user_id=user_id)