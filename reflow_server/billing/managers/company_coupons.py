from django.db import models
from django.db.models import Q
from django.utils import timezone


class CompanyCouponsBillingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def create(self, company_id, discount_coupon_id):
        """
        Creates a new discount coupon for the company. If the company has discount coupons
        he will have discounts from the total he on our platform.

        Args:
            company_id (int): A reflow_server.authentication.models.Company instance id
            discount_coupon_id (int): A reflow_server.billing.models.DiscountCoupon instance id, this
            is the coupon the company will use.

        Returns:
            reflow_server.billing.models.CompanyCoupons: The created CompanyCoupons instance
        """
        instance = self.get_queryset().create(
            company_id=company_id,
            discount_coupon_id=discount_coupon_id
        )
        return instance

    def company_coupons_by_company_id(self, company_id):
        """
        Retrieves a queryset of CompanyCoupons from a company_id

        Args:
            company_id (int): A reflow_server.authentication.models.Company instance id

        Returns:
            django.db.models.QuerySet(reflow_server.billing.models.CompanyCoupons): A queryset of company coupons that the
            company have available for usage.
        """
        return self.get_queryset().filter(
            Q(company_id=company_id, discount_coupon__permanent=True) |
            Q(company_id=company_id, discount_coupon__permanent=False, discount_coupon__end_at__lte=timezone.now(), discount_coupon__start_at__gte=timezone.now())
        )