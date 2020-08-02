from django.db.models import Q, Sum

from reflow_server.billing.models import CompanyCoupons, DiscountCoupon

from datetime import datetime
import numpy
import functools


class CompanyChargeData:
    def __init__(self, individual_value_charge_name , quantity, user_id=None):
        self.charge_name = individual_value_charge_name
        self.quantity = quantity
        self.user_id = user_id
        

class IndividualCompanyChargeData:
    def __init__(self, individual_value_charge_name, individual_value_charge, quantity, individual_discount=1.0):
        """
        This class is just used to hold each individual company charge data, so the individual charge name, with it's
        individual charge value, the quantity of the items and the individual discout. It's basically a map of each row of a company
        in reflow_server.billing.models.CurrentCompanyCharge. 
        This object is also responsible for calculating each of those rows. 

        Args:
            individual_value_charge_name (str): IndividualChargeValueType name field
            individual_value_charge (float/int): IndividualChargeValueType value field
            quantity (int): The quantity of each individual item
            individual_discount (float, optional): The discount percentage of the individual value. 
                                                   For example, for a 10% discount the value should be 0.9 and not 0.1 Defaults to 1.
        """
        self.charge_name = individual_value_charge_name
        self.charge_value = individual_value_charge
        self.quantity = quantity
        self.charge_discount_percentage = individual_discount

    @property
    def get_total(self):
        """
        Basically the formula of our billing, really simple, just the discount multiplied by the quantity and each individual value.

        Returns:
            float: The total of this row basically
        """
        return float(self.quantity) * float(self.charge_value) * float(self.charge_discount_percentage)


class TotalData:
    def __init__(self, company_id):
        self.individual_value_charges_by_name = {}
        self.discount_coupons = CompanyCoupons.objects.filter(
            Q(company_id=company_id, discount_coupon__permanent=True) |
            Q(company_id=company_id, discount_coupon__end_at__lte=datetime.now(), discount_coupon__start_at__gte=datetime.now())
        )

    def add_value(self, individual_value_charge_name, individual_value_charge, quantity, individual_discount=1):
        """
        Do not use this method anyware outside billing services
        """
        existing_values = self.individual_value_charges_by_name.get(individual_value_charge_name, list())
        existing_values = existing_values + [IndividualCompanyChargeData(individual_value_charge_name, individual_value_charge, quantity, individual_discount)]
        self.individual_value_charges_by_name[individual_value_charge_name] = existing_values
        return self.individual_value_charges_by_name

    @property
    def total_coupons_discounts(self):
        """
        Gets the total of the discounts by company coupons, we can send coupons to companies so they can have
        discounts while using our platform. This gets the total of the discount coupons so we can subtract from the total.

        Returns:
            float: a float with the total of discounts
        """
        discounts_aggregate_result = self.discount_coupons.aggregate(total_coupons_discount=Sum('discount_coupon__value')).get('total_coupons_discount', 0)
        return discounts_aggregate_result if discounts_aggregate_result else 0

    @property
    def total_by_charge_name(self):
        """
        Gets the total by each charge_name of the company.

        Returns:
            dict: A dict containing each reflow_server.billing.models.IndividualChargeValueType names as keys and the total as values
        """
        total_by_charge_name = dict()
        for key in self.individual_value_charges_by_name.keys():
            individual_company_charge_values = [float(individual_value_charge_value.get_total) for individual_value_charge_value in self.individual_value_charges_by_name[key]]
            if len(individual_company_charge_values) > 0:
                total_by_charge_name[key] = functools.reduce(lambda x, y: float(x) + float(y), numpy.asarray(individual_company_charge_values))
            else:
                total_by_charge_name[key] = 0
        return total_by_charge_name

    @property
    def total(self):
        total = 0
        totals = [value for value in self.total_by_charge_name.values()]
        if len(totals) > 0:
            total = functools.reduce(lambda x, y: float(x) + float(y), numpy.asarray(totals))
        total = total - float(self.total_coupons_discounts)
        total = 0 if total < 0 else total
        return total
