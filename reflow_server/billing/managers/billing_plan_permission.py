from django.db import models

class BillingPlanPermissionBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
    def exists_has_soft_limit_by_plan_id_and_individual_charge_value_type_name(self, plan_id, individual_charge_value_type_name):
        return self.get_queryset().filter(
            billing_plan_id=plan_id, 
            individual_charge_value_type__name=individual_charge_value_type_name,
            has_soft_limit=True
        ).exists()

    def plan_increase_by_plan_id_and_individual_charge_value_type_id(self, billing_plan_id, individual_charge_value_type_id):
        return self.get_queryset().filter(
            billing_plan_id=billing_plan_id, 
            individual_charge_value_type_id=individual_charge_value_type_id
        ).values_list('price_multiplicator', flat=True).first()

    def billing_plan_permissions_by_plan_id(self, billing_plan_id):
        return self.get_queryset().filter(billing_plan_id=billing_plan_id)