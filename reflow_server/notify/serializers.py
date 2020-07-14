from rest_framework import serializers

from reflow_server.notify.relations import MailRelation, PushRelation


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
