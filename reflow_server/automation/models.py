from django.db import models

import uuid


class AutomationInputFieldType(models.Model):
    name = models.CharField(max_length=280)
    order = models.BigIntegerField()

    class Meta:
        db_table = 'automation_input_field_type'
        ordering = ('order',)


class TriggerType(models.Model):
    name = models.CharField(max_length=280)
    order = models.BigIntegerField()
 
    class Meta:
        db_table = 'trigger_type'
        ordering = ('order',)


class AutomationApp(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    website = models.CharField(max_length=500)
    logo_url = models.CharField(max_length=500)
    integration_authentication = models.ForeignKey('integration.IntegrationAuthentication', on_delete=models.CASCADE, null=True)
        
    class Meta:
        db_table = 'automation_app'


class AutomationAppTrigger(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    script = models.TextField()
    automation_app = models.ForeignKey('automation.AutomationApp', on_delete=models.CASCADE)
    input_formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE)
    trigger_type = models.ForeignKey('automation.TriggerType', on_delete=models.CASCADE)
    trigger_webhook = models.CharField(max_length=500)

    class Meta:
        db_table = 'automation_app_trigger'


class AutomationAppAction(models.Model):
    name = models.CharField(max_length=400)
    description = models.TextField()
    script = models.TextField()
    automation_app = models.ForeignKey('automation.AutomationApp', on_delete=models.CASCADE)
    input_formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE)

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
    formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE)
    show_section_name = models.BooleanField(default=True)

    class Meta:
        db_table = 'automation_input_section'


class AutomationInputField(models.Model):
    name = models.CharField(max_length=300)
    is_required = models.BooleanField(default=False)
    section = models.ForeignKey('automation.AutomationInputSection', on_delete=models.CASCADE)
    field_type = models.ForeignKey('automation.AutomationInputFieldType', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation_input_field'


class AutomationInputDataFormulary(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    formulary = models.ForeignKey('automation.AutomationInputFormulary', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation_input_data_formulary'


class AutomationInputDataSection(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    formulary_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE)
    section = models.ForeignKey('automation.AutomationInputSection', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation_input_data_section'


class AutomationInputDataFieldValue(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    section_data = models.ForeignKey('automation.AutomationInputDataSection', on_delete=models.CASCADE)
    formulary_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE)
    field = models.ForeignKey('automation.AutomationInputField', on_delete=models.CASCADE)
    value = models.TextField()
    
    class Meta:
        db_table = 'automation_input_data_field_value'


class Automation(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=500)
    description = models.TextField()
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE)

    class Meta:
        db_table = 'automation'


class AutomationTrigger(models.Model):
    automation = models.OneToOneField('automation.Automation', on_delete=models.CASCADE)
    app_trigger = models.ForeignKey('automation.AutomationAppTrigger', on_delete=models.CASCADE)
    input_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'automation_trigger'


class AutomationAction(models.Model):
    automation = models.ForeignKey('automation.Automation', on_delete=models.CASCADE)
    app_action = models.ForeignKey('automation.AutomationAppAction', on_delete=models.CASCADE)
    input_data = models.ForeignKey('automation.AutomationInputDataFormulary', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'automation_action'