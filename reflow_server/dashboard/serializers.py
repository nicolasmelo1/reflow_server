from rest_framework import serializers


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