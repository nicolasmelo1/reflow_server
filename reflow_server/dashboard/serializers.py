from rest_framework import serializers

from reflow_server.dashboard.models import DashboardChartConfiguration
from reflow_server.formulary.models import Field


class DashboardDataSerializer(serializers.Serializer):
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
    id = serializers.IntegerField(required=False, allow_null=True)
    
    class Meta:
        model = DashboardChartConfiguration
        fields = ('id', 'name', 'for_company', 'value_field', 'label_field', 'number_format_type', 'chart_type', 'aggregation_type')


class DashboardFieldsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    field_type = serializers.CharField(source='type.type')

    class Meta:
        model = Field
        fields = ('id', 'name', 'field_type', 'label_name')