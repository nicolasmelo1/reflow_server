from rest_framework import serializers


class MailVariablesRelation(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class MailRelation(serializers.Serializer):
    subject = serializers.CharField()
    recipient = serializers.CharField()
    variables = MailVariablesRelation(required=False, many=True)


class PushTokenRelation(serializers.Serializer):
    token = serializers.CharField()
    type = serializers.CharField()


class PushVariablesRelation(serializers.Serializer):
    name = serializers.CharField()
    value = serializers.CharField()


class PushVariableRelation(serializers.Serializer):
    title = PushVariablesRelation(many=True)
    body = PushVariablesRelation(many=True)


class PushRelation(serializers.Serializer):
    tokens = PushTokenRelation(many=True)
    variables = PushVariableRelation()