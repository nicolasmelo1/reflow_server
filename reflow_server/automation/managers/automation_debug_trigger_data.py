from django.db import models


class AutomationDebugTriggerDataAutomationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create_or_update_debug_trigger_data(self, data_stringfied, debug_trigger_data_id=None):
        instance, __ = self.get_queryset().update_or_create(
            id=debug_trigger_data_id,
            defaults={
                'debug_as_string': data_stringfied
            }
        )
        return instance