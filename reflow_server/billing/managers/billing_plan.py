from django.db import models

class BillingPlanBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def all_plans(self):
        return self.get_queryset().all()

    def starter_plan_id(self):
        return self.get_queryset().filter(name='Starter').values_list('id', flat=True).first()