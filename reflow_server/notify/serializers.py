from rest_framework import serializers

from reflow_server.notify.relations import MailRelation, PushRelation
from reflow_server.notify.models import PushNotification, PushNotificationTagType


class MailSerializer(serializers.Serializer):
    from_email = serializers.CharField()
    template = serializers.CharField()
    recipients = MailRelation(many=True)

    def __init__(self, *args, **kwargs):
        super(MailSerializer, self).__init__(*args, **kwargs)
        self.is_valid()


class PushSerializer(serializers.Serializer):
    template = serializers.CharField()
    recipients = PushRelation(many=True)

    def __init__(self, *args, **kwargs):
        super(PushSerializer, self).__init__(*args, **kwargs)
        self.is_valid()


class PushNotificationRegistrationSerializer(serializers.ModelSerializer):
    """
    This serializer is responsible for registering push notifications endpoints
    """
    endpoint = serializers.CharField()
    push_notification_tag_type_name = serializers.CharField(source='push_notification_tag_type.name')
    token = serializers.CharField()

    def save(self, user_id):
        instance, __ = PushNotification.objects.update_or_create(
            endpoint=self.validated_data['endpoint'],
            push_notification_tag_type=PushNotificationTagType.objects.filter(name=self.validated_data['push_notification_tag_type']['name']).first(),
            token=self.validated_data['token'],
            user_id=user_id
        )
        return instance

    class Meta:
        model = PushNotification
        fields = ('endpoint', 'push_notification_tag_type_name', 'token')
