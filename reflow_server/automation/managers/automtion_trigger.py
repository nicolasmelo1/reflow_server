from django.db import models


class AutomationTriggerAutomationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def debug_data_id_by_automation_id(self, automation_id):
        return self.get_queryset().filter(
            automation_id=automation_id
        ).values_list('debug_data_id', flat=True).first()