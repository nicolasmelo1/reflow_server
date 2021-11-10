from django.db import models


class SurveyAnalyticsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def survey_by_id(self, survey_id):
        """
        Retrives a survey by it's id.

        Args:
            survey_id (int): The id of the survey to retrieve.

        Returns:
            reflow_server.analytics.models.Survey: The survey retrieved from the given id.
        """
        return self.get_queryset().filter(id=survey_id).first()

    def active_surveys_id_time_in_minutes_for_retaking_and_criteria_function_name(self):
        return self.get_queryset().filter(is_active=True).values('id', 'time_in_minutes_for_retaking', 'criteria_function_name')