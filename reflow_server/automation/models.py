from django.db import models

from reflow_server.automation.managers import AutomationDebugTriggerDataAutomationManager, \
    AutomationTriggerAutomationManager


import uuid


class AutomationInputSectionType(models.Model):
    """
    This is the type of section of the input formulary, similar to how reflow operates
    the automation works in a similar way. The idea is that we can have multiple sections (lists)
    or single and unique sections. This is used so we can have dynamic data in our sections.
    """
    name = models.CharField(max_length=280)
    order = models.BigIntegerField()

    class Meta:
        db_table = 'automation_input_section_type'
        ordering = ('order',)


class AutomationInputFieldType(models.Model):
    """
    This is each type of field in the input formulary of automations.
    If you look closely we do not use field_types and you might ask yourself why.

    That's because in automation forms we have a smaller version of Reflow formularies but
    without many stuff in reflow, Automations work like their own little universe.
    """
    name = models.CharField(max_length=280)
    order = models.BigIntegerField()

    class Meta:
        db_table = 'automation_input_field_type'
        ordering = ('order',)


class TriggerType(models.Model):
    """
    The type of trigger, we will have 2 types planed but we can extend:
    Hooks and Pooling. Hooks works in realtime we recieve the user id and the name of the event
    as well the data and then we do something with it.
    """
    name = models.CharField(max_length=280)
    order = models.BigIntegerField()
 
    class Meta:
        db_table = 'trigger_type'
        ordering = ('order',)


class AutomationApp(models.Model):
    """
    This is the app of the automation, the app of the automation will hold all of the triggers of an app
    and all of the actions, the app is linked to IntegrationAuthentication because we hold the authentication for external
    apps inside of the `integration` domain. The idea is that after the user has authenticated with an application
    he should not need to log in again.

    Also the idea is that integrations should not be bounded to apps only but every aspect of the application that
    we will want to apply integrations, want to integrate a field a visualization, a formula and all that stuff
    just log once and you are good to go.

    The automation apps so is composed of Triggers and Actions, it also holds the flow context so we can also translate
    automation scripts for triggers and actions. Each trigger and each action is just a Flow Script that will run from time
    to time or when a webhook is called.
    """
    name = models.CharField(max_length=500)
    label_name = models.CharField(max_length=500)
    app_color = models.CharField(max_length=400, default='#0dbf7e')
    flow_context = models.ForeignKey('formula.FormulaContextType', on_delete=models.CASCADE, null=True)
    description = models.TextField()
    website = models.CharField(max_length=500)
    logo_url = models.CharField(max_length=500, null=True)
    is_internal_app = models.BooleanField(default=False)
    integration_authentication = models.ForeignKey('integration.IntegrationAuthentication', on_delete=models.CASCADE, null=True)
        
    class Meta:
        db_table = 'automation_app'


class AutomationAppTrigger(models.Model):
    """
    This is each trigger from the app. This will be each trigger from a specific app. 
    A trigger is nothing more of an custom flow script, this custom flow script is responsible
    for calling the Automation.trigger_action({}) sending the data from the trigger, the data 
    that you send must follow a specific pattern.

    The idea of this is that the programmer who is creating the app trigger will be responsible for checking
    the difference between the last pool data and the new pool data. Also the programmer will be responsible for
    activating the trigger.

    This will all be done with a flow script in the translation that he will feel most familiar with, we will not force
    him to use any language or whatever, the idea is that in the future normal users (not programmers anymore) should be
    able to create apps with triggers and actions so they can solve all of their issues.
    """
    name = models.CharField(max_length=400)
    description = models.TextField()
    script = models.TextField()
    automation_app = models.ForeignKey('automation.AutomationApp', on_delete=models.CASCADE, related_name='automation_app_triggers')
    input_formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE, null=True)
    embbed_formulary_url = models.TextField(null=True)
    trigger_type = models.ForeignKey('automation.TriggerType', on_delete=models.CASCADE)
    trigger_webhook = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'automation_app_trigger'


class AutomationAppAction(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    script = models.TextField()
    automation_app = models.ForeignKey('automation.AutomationApp', on_delete=models.CASCADE, related_name='automation_app_actions')
    input_formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE, null=True)
    embbed_formulary_url = models.TextField(null=True)
    enable_custom_script = models.BooleanField(default=False)

    class Meta:
        db_table = 'automation_app_action'


class AutomationPooling(models.Model):
    pool_id = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    company_id = models.ForeignKey('authentication.Company', on_delete=models.CASCADE)
    next_pool = models.DateTimeField(auto_now_add=True)
    pool_data = models.TextField()
    has_evaluated = models.BooleanField(default=False)

    class Meta:
        db_table = 'automation_pooling'


class AutomationInputFormulary(models.Model):
    name = models.CharField(max_length=280)
    
    class Meta:
        db_table = 'automation_input_formulary'


class AutomationInputSection(models.Model):
    name = models.CharField(max_length=280)
    formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE, related_name='formulary_sections')
    show_section_name = models.BooleanField(default=True)
    section_type = models.ForeignKey('automation.AutomationInputSectionType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation_input_section'


class AutomationInputField(models.Model):
    name = models.CharField(max_length=300)
    is_required = models.BooleanField(default=False)
    section = models.ForeignKey('automation.AutomationInputSection', on_delete=models.CASCADE, related_name='section_fields')
    field_type = models.ForeignKey('automation.AutomationInputFieldType', on_delete=models.CASCADE)
    script_to_load_data = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'automation_input_field'


class AutomationInputFieldConditionsToReload(models.Model):
    """
    This model is just a relation many-to-many, the idea is that this will be check which fields have to be changed in order to reload a field.

    Suppose we have a form like:

    >>> Select the page
    >>> Select the section
    >>> select the field

    The last field will depend on both page and section changing to reload, otherwise it will not reload.
    """
    field = models.ForeignKey('automation.AutomationInputField', on_delete=models.CASCADE, related_name='field_conditions_to_reload')
    condition = models.ForeignKey('automation.AutomationInputField', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation_input_field_conditions_to_reload'


class AutomationInputFieldOption(models.Model):
    """
    This is the automation field option if the field type is a select field type.
    This is similar to `option` type of fields in reflow but in a smaller form factor in reflow.
    """
    field = models.ForeignKey('automation.AutomationInputField', on_delete=models.CASCADE, related_name='field_field_options')
    option = models.CharField(max_length=500, db_index=True)
    order = models.BigIntegerField()

    class Meta:
        db_table = 'automation_input_field_option'
        ordering = ('order',)


class AutomationInputDataFormulary(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation_input_data_formulary'


class AutomationInputDataSection(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    formulary_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE, related_name='formulary_record_sections')
    section = models.ForeignKey('automation.AutomationInputSection', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation_input_data_section'


class AutomationInputDataFieldValue(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    section_data = models.ForeignKey('automation.AutomationInputDataSection', on_delete=models.CASCADE, related_name='section_record_fields')
    formulary_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE)
    field = models.ForeignKey('automation.AutomationInputField', on_delete=models.CASCADE)
    value = models.TextField()
    
    class Meta:
        db_table = 'automation_input_data_field_value'


class AutomationTriggerLog(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    trigger = models.ForeignKey('automation.AutomationTrigger', on_delete=models.CASCADE)
    result = models.TextField()

    class Meta:
        db_table = 'automation_trigger_log'


class AutomationActionLog(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    action = models.ForeignKey('automation.AutomationAction', on_delete=models.CASCADE)
    result = models.TextField()

    class Meta:
        db_table = 'automation_action_log'


class Automation(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE)
    user = models.ForeignKey('authentication.UserExtended', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'automation'
 

class AutomationDebugTriggerData(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    data_as_string = models.TextField()

    class Meta:
        db_table = 'automation_debug_trigger_data'

    automation_ = AutomationDebugTriggerDataAutomationManager()


class AutomationTrigger(models.Model):
    automation = models.OneToOneField('automation.Automation', on_delete=models.CASCADE, related_name='automation_trigger')
    app_trigger = models.ForeignKey('automation.AutomationAppTrigger', on_delete=models.CASCADE)
    input_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE, null=True)
    debug_data = models.ForeignKey('automation.AutomationDebugTriggerData', on_delete=models.SET_NULL, null=True)
    
    class Meta:
        db_table = 'automation_trigger'

    automation_ = AutomationTriggerAutomationManager


class AutomationAction(models.Model):
    automation = models.ForeignKey('automation.Automation', on_delete=models.CASCADE, related_name='automation_actions')
    app_action = models.ForeignKey('automation.AutomationAppAction', on_delete=models.CASCADE)
    input_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE, null=True)
    custom_script = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'automation_action'