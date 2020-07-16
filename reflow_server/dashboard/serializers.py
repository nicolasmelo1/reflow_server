from rest_framework import serializers

from reflow_server.dashboard.models import DashboardChartConfiguration
from reflow_server.formulary.models import Field


class DashboardChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardChartConfiguration
        fields = ('id', 'name', 'number_format_type', 'chart_type')


class DashboardDataSerializer(serializers.Serializer):
    """
    This serializer is used for retriving the aggregated data to the user. It uses the data
    recieved from the AggregationService from the `data` app.
    """
    labels = serializers.ListField(allow_empty=True)
    values = serializers.ListField(allow_empty=True)

    def __init__(self, dashboard_data, *args, **kwargs):
        kwargs['data']={
            'labels': list(dashboard_data.keys()),
            'values': list(dashboard_data.values())
        }
        super(DashboardDataSerializer, self).__init__(*args, **kwargs)
        self.is_valid()


class DashboardChartConfigurationSerializer(serializers.ModelSerializer):
    """
    This is a serializer for updating, creating and retrieving DashboardChartConfiguration
    This is only used when configuring a new chart in the dashboard.
    """
    id = serializers.IntegerField(required=False, allow_null=True)

    def save(self, company_id, form_id, user_id):
        instance, __ = DashboardChartConfiguration.objects.update_or_create(
            id=self.instance.id if self.instance else None,
            defaults={
                'name': self.validated_data['name'],
                'for_company': self.validated_data['for_company'],
                'value_field': self.validated_data['value_field'],
                'label_field': self.validated_data['label_field'],
                'number_format_type': self.validated_data['number_format_type'],
                'chart_type': self.validated_data['chart_type'],
                'aggregation_type': self.validated_data['aggregation_type'],
                'company_id': company_id,
                'form_id': form_id,
                'user_id': user_id
            }
        )
        return instance

    class Meta:
        model = DashboardChartConfiguration
        # adds custom messages, the default error messages are not that useful, we want the error message to be more "dumb"
        # so the user interface can parse better https://stackoverflow.com/a/26975268/13158385
        extra_kwargs = { field : {'error_messages': {'null': 'blank', 'blank': 'blank'}} for field in ('id', 'name', 'for_company', 'value_field', 'label_field', 'number_format_type', 'chart_type', 'aggregation_type') }
        fields = ('id', 'name', 'for_company', 'value_field', 'label_field', 'number_format_type', 'chart_type', 'aggregation_type')


class DashboardFieldsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    field_type = serializers.CharField(source='type.type')

    class Meta:
        model = Field
        fields = ('id', 'name', 'type', 'field_type', 'label_name')