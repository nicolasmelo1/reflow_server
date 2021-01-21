from django.db import models
from django.db.models import Q
from django.utils import timezone


class DiscountCouponBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def discount_coupon_id_by_coupon_name(self, coupon_name):
        """
        Retrieves the id of a DiscountCoupon so we can use it elsewhere

        Args:
            coupon_name (str): The name of the coupon we use, we use the first we find.

        Returns:
            int: The id of the instance found based on the conditions
        """
        return self.get_queryset().filter(
            Q(name=coupon_name, permanent=True) |
            Q(name=coupon_name, permanent=False, start_at__gte=timezone.now(), end_at__lte=timezone.now())
        ).values_list('id', flat=True).first()