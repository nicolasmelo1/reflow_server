from django.db import models

class BillingPlanBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def all_plans(self):
        return self.get_queryset().all()

    def is_plan_id_freemium(self, plan_id):
        return self.get_queryset().filter(name='Free', id=plan_id).exists()

    def starter_plan_id(self):
        return self.get_queryset().filter(name='Starter').values_list('id', flat=True).first()