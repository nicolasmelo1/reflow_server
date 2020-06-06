from rest_framework import serializers

from reflow_server.notify.relations import MailRelation, PushRelation


class MailSerializer(serializers.Serializer):
    from_mail = serializers.CharField()
    template = serializers.CharField()
    recipients = MailRelation(many=True)


class PushSerializer(serializers.Serializer):
    template = serializers.CharField()
    recipients = PushRelation(many=True)