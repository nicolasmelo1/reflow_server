from rest_framework import serializers

from reflow_server.automation.models import AutomationApp, AutomationInputFormulary
from reflow_server.automation.relations import AutomationAppTriggerRelation, AutomtionAppActionRelation, \
    AutomationInputSectionRelation


class AutomationAppsSerializer(serializers.ModelSerializer):
    automation_app_triggers = AutomationAppTriggerRelation(many=True)
    automation_app_actions = AutomtionAppActionRelation(many=True)
    
    class Meta:
        model = AutomationApp
        fields = '__all__'


class AutomationInputFormularySerializer(serializers.ModelSerializer):
    formulary_sections = AutomationInputSectionRelation(many=True)

    class Meta:
        model = AutomationInputFormulary
        fields = '__all__'
