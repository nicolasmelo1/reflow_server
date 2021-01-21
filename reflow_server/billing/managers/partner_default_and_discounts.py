from django.db import models


class PartnerDefaultAndDiscountsBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def partner_default_and_discounts_by_partner_name(self, partner_name):
        return self.get_queryset().filter(partner_name=partner_name)

    def partner_default_and_discount_by_partner_name_and_individual_charge_value_type_id(self, partner_name, individual_charge_value_type_id):
        return self.get_queryset().filter(partner_name=partner_name, individual_charge_value_type_id=individual_charge_value_type_id).first()
