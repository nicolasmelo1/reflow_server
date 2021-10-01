from rest_framework import serializers

from reflow_server.automation.models import AutomationAppTrigger, AutomationAppAction, \
    AutomationInputSection, AutomationInputField, AutomationInputFieldConditionsToReload, \
    AutomationInputFieldOption


class AutomtionAppActionRelation(serializers.ModelSerializer):
    class Meta:
        model = AutomationAppAction
        exclude = ('automation_app', 'script')


class AutomationAppTriggerRelation(serializers.ModelSerializer):
    class Meta:
        model = AutomationAppTrigger
        exclude = ('automation_app', 'trigger_type', 'trigger_webhook', 'script')


class AutomationInputFieldConditionsToReloadRelation(serializers.ModelSerializer):
    class Meta:
        model = AutomationInputFieldConditionsToReload
        fields = '__all__'


class AutomationInputFieldOptionRelation(serializers.ModelSerializer):
    class Meta:
        model = AutomationInputFieldOption
        fields = '__all__'


class AutomationInputFieldRelation(serializers.ModelSerializer):
    field_conditions_to_reload = AutomationInputFieldConditionsToReloadRelation(many=True)
    field_field_options = AutomationInputFieldOptionRelation(many=True)
    
    class Meta:
        model = AutomationInputField
        exclude = ('section',)


class AutomationInputSectionRelation(serializers.ModelSerializer):
    section_fields = AutomationInputFieldRelation(many=True)

    class Meta:
        model = AutomationInputSection
        exclude = ('formulary',)