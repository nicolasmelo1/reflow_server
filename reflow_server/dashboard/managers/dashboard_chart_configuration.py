from django.db import models


class DashboardChartConfigurationDashboardManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def count_dashboard_chart_configuration_by_form_name_and_company_id_excluding_dashboard_configuration_id(self, form_name, company_id, dashboard_configuration_id):
        return self.get_queryset().filter(
            company_id=company_id, 
            form__form_name=form_name
        ).exclude(id=dashboard_configuration_id).count()