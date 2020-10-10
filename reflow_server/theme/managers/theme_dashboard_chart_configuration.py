from django.db import models


class ThemeDashboardChartConfigurationThemeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def theme_dashboard_chart_configuration_by_theme_id_ordered(self, theme_id):
        """
        Retrieves all of the ThemeDashboardChartConfiguration from a single theme_id.
        It retrieves them ORDERED by id on an ascending order. (smallest ids first)

        Args:
            theme_id (int): A Theme instance id

        Returns:
            django.db.models.QuerySet(reflow_server.theme.models.ThemeDashboardChartConfiguration): This
            is a queryset of ThemeDashboardChartConfiguration instances from a single theme
        """
        return self.get_queryset().filter(theme_id=theme_id).order_by('id')

    def create_theme_dashboard_chart_configuration(self, name, for_company, value_theme_field_id, label_theme_field_id, 
                                                   number_format_type_id, chart_type_id, aggregation_type_id, theme_form_id, 
                                                   theme_id):
        return self.get_queryset().create(
            label_field_id=label_theme_field_id,
            value_field_id=value_theme_field_id,
            form_id=theme_form_id,
            theme_id=theme_id,
            name=name,
            for_company=for_company,
            aggregation_type_id=aggregation_type_id,
            chart_type_id=chart_type_id,
            number_format_type_id=number_format_type_id
        )