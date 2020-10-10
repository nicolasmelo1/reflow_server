from django.db import models


class DashboardChartConfigurationThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def dashboard_chart_configurations_by_company_id_main_form_ids_user_id_for_hole_company_ordered(self, company_id, main_form_ids, user_id):
        """
        Retrieves all of the DashboardChartConfiguration from the company it resides, a list of main form ids that
        the dashboard chart migh be from and from a single user that are for the hole company.
        It retrieves them ORDERED by id on an desceding order. (biggest ids first)

        Args:
            user_id (int): A UserExtended instance id, this is used to filter DashboardChartConfiguration for a specific user.
            company_id (int): A Company instance id, from which company is this dashboard chart configuration
            main_form_ids (list(int)): The formularies ids to filter the dashboard charts

        Returns:
            django.db.models.QuerySet(reflow_server.dashboard.models.DashboardChartConfiguration): A queryset of DashboardChartConfiguration
            instances that the hole company has access to.
        """
        return self.get_queryset().filter(
            label_field__form__depends_on__group__company_id=company_id, 
            label_field__form__depends_on__in=main_form_ids, 
            user_id=user_id, 
            for_company=True
        ).order_by('-id')