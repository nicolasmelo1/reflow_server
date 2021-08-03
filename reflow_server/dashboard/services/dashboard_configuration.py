from reflow_server.core.events import Event
from reflow_server.dashboard.models import DashboardChartConfiguration
from reflow_server.dashboard.services.permissions import DashboardPermissionsService


class DashboardChartConfigurationService:
    def __init__(self, company_id, user_id, form):
        """
        Service responsible for handling dashboard charts configuration.

        Args:
            company_id (int): A Company instance id. This is the company that is editing this dashboard configuration.
            user_id (int): A UserExtended instance id. This is the user that is editing or creating this chart.
            form (reflow_server.formulary.models.Form): The Form instance of what formulary is this dashboard.
            Keep in mind this is MAIN FORMS not sections.
        """
        self.company_id = company_id
        self.user_id = user_id
        self.form = form

    def create_or_update(self, name, for_company, value_field, label_field, number_format_type, chart_type, 
                         aggregation_type, dashboard_configuration_id=None):
        """
        Create or updates a DashboardChartConfiguration instance. It's important to notice that here we validate the billing also before saving.
        We do this because of the templates, the templates does not need to care of how many dashboards you can create. 
        You will notice that we use this function twice on the same request, (on permissions and here). We cannot validate while saving, so mostly
        here is kinda useless and adds an overhead to the code.

        Args:
            name (int): Just a description and user friendly name for the dashboard chart, setted by the user
            for_company (bool): Sets the dashboard configuration for the hole company 
            value_field (reflow_server.formulary.models.Field): The field to use as the value of the aggregation
            label_field (reflow_server.formulary.models.Field): The field to use as the label/key of the aggregation
            number_format_type (reflow_server.formulary.models.FieldNumberFormatType): The FieldNumberFormatType, or how to format the values
            of the aggregation
            chart_type (reflow_server.dashboard.models.ChartType): What is the chart_type, is it a pie, a bar, or a line?
            aggregation_type (reflow_server.dashboard.models.AggregationType): How to aggregate the values of value_field
            dashboard_configuration_id (int, optional): If you are editing an DashboardChartConfiguration instance, you need
            to define the id. Defaults to None.

        Returns:
            reflow_server.dashboard.models.DashboardChartConfiguration: The DashboardChartConfiguration created instance
        """

        if DashboardPermissionsService.is_valid_billing_charts(self.company_id, self.user_id, self.form.form_name, for_company, dashboard_configuration_id):
            instance, was_created = DashboardChartConfiguration.objects.update_or_create(
                id=dashboard_configuration_id,
                defaults={
                    'name': name,
                    'for_company': for_company,
                    'value_field': value_field,
                    'label_field': label_field,
                    'number_format_type': number_format_type,
                    'chart_type': chart_type,
                    'aggregation_type': aggregation_type,
                    'company_id': self.company_id,
                    'form_id': self.form.id,
                    'user_id': self.user_id
                }
            )

            # sends events that a dashboard chart was created or that a chart was updated.
            events_data = {
                'user_id': self.user_id,
                'company_id': self.company_id,
                'form_id': self.form.id,
                'dashboard_chart_id': instance.id
            }
            
            if was_created:
                Event.register_event('dashboard_chart_created', events_data)
            else:
                Event.register_event('dashboard_chart_updated', events_data)
            return instance
        else:
            return None

