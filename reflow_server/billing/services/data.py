from django.db.models import Sum

from reflow_server.billing.models import CompanyCoupons, IndividualChargeValueType
from reflow_server.authentication.models import UserExtended

import functools
import numpy


class CompanyChargeData:
    def __init__(self, individual_value_charge_name, quantity):
        """
        This is used for retrieving the totals when the company charge data is not saved in the database, so the user
        can have a feedback on the totals when he changes the billing information on the frontend

        Args:
            individual_value_charge_name (str): The individual value charge name 
            charge_type_name (str): The charge type, can be user or company
            quantity (int): The quantity for each individual_value_charge
        """
        individual_charge_value_type = IndividualChargeValueType.objects.filter(name=individual_value_charge_name).first()
        self.charge_type_name = individual_charge_value_type.charge_type.name if individual_charge_value_type else None
        self.individual_value_charge_id = individual_charge_value_type.id if individual_charge_value_type else None
        self.individual_value_charge_name = individual_value_charge_name
        self.quantity = quantity
        

class IndividualCompanyChargeData:
    def __init__(self, individual_value_charge_name, charge_type_name, individual_value_charge_value, total_number_of_users_of_company, quantity, individual_discount=1.0):
        """
        This class is just used to hold each individual company charge data, so the individual charge name, with it's
        individual charge value, the quantity of the items and the individual discout. It's basically a map of each row of a company
        in reflow_server.billing.models.CurrentCompanyCharge. 
        This object is also responsible for calculating each of those rows. 

        Args:
            individual_value_charge_name (str): IndividualChargeValueType name field
            charge_type_name (str): The ChargeType of the individual charge value type, it can be 'user' or 'company'
            individual_value_charge_value (float/int): IndividualChargeValueType value field
            total_number_of_users_of_company (int): The total number of users of the company, so we can multiply it by individual_value_charge of type `user`
            quantity (int): The quantity of each individual item
            individual_discount (float, optional): The discount percentage of the individual value. 
                                                   For example, for a 10% discount the value should be 0.9 and not 0.1 Defaults to 1.
        """
        self.charge_type_name = charge_type_name
        self.total_number_of_users_of_company = total_number_of_users_of_company
        self.individual_value_charge_name = individual_value_charge_name
        self.individual_value_charge_value = individual_value_charge_value
        self.quantity = quantity
        self.charge_discount_percentage = individual_discount

    @property
    def get_total(self):
        """
        Basically the formula of our billing, really simple, just the discount multiplied by the quantity and each individual value.

        Returns:
            float: The total of this row basically
        """
        value = float(self.quantity) * float(self.individual_value_charge_value) * float(self.charge_discount_percentage)
        if self.charge_type_name == 'user':
            value = value * self.total_number_of_users_of_company
        return value

class TotalData:
    def __init__(self, company_id):
        """
        Responsible for calculating the total charge of a company.
        
        How to use it:
        1 - You need to add values using the `.add_value()` function
        2 - You can get the aggregated total using `.total`, the coupons discount using `.total_coupons_discounts` and
        the by each individual charge name using `total_by_charge_name`

        Args:
            company_id (int): The company
        """
        self.individual_value_charges_by_name = {}
        self.total_users_of_company = UserExtended.billing_.users_active_by_company_id(company_id=company_id).count()
        self.discount_coupons = CompanyCoupons.billing_.company_coupons_by_company_id(company_id)

    def add_value(self, individual_value_charge_name, charge_type_name, individual_value_charge, quantity, individual_discount=1):
        """
        This method is for adding data and generate a TotalData object with handy functions you can use for totals.
        """
        self.individual_value_charges_by_name[individual_value_charge_name] = IndividualCompanyChargeData(
            individual_value_charge_name, 
            charge_type_name, 
            individual_value_charge,
            self.total_users_of_company,
            quantity, 
            individual_discount
        )
        return self.individual_value_charges_by_name

    @property
    def total_coupons_discounts(self):
        """
        Gets the total of the discounts by company coupons, we can send coupons to companies so they can have
        discounts while using our platform. This gets the total of the discount coupons so we can subtract from the total.

        IMPORTANT: The coupons can be a percentage or can be full. If percentage, this means we give X% discount for companies. If full
        this means we give $X discount for companies.

        Returns:
            dict(): {
                full: float - The full value the user have as discount.
                percentage: float - The percentage the user have as discount.
            }
        """
        # These are the full values, like $25 in discount
        discounts_aggregate_sum_result = self.discount_coupons.filter(discount_coupon__value__gte=1).aggregate(total_coupons_discount=Sum('discount_coupon__value')).get('total_coupons_discount', 0)
        # These are the percentage discount values, like 10% of discount.
        discount_percentages = self.discount_coupons.filter(discount_coupon__value__lt=1)
        discounts_aggregate_multiply_result = 1
        for discount_percentage in discount_percentages:
            discounts_aggregate_multiply_result = discounts_aggregate_multiply_result * discount_percentage.value
        return {
            'full': float(discounts_aggregate_sum_result) if discounts_aggregate_sum_result else 0,
            'percentage': discounts_aggregate_multiply_result
        }

    @property
    def total_by_charge_name(self):
        """
        Gets the total by each charge_name of the company.

        Returns:
            dict: A dict containing each reflow_server.billing.models.IndividualChargeValueType names as keys and the total as values
        """
        total_by_charge_name = dict()
        for key in self.individual_value_charges_by_name.keys():
            value = float(self.individual_value_charges_by_name[key].get_total)
            total_by_charge_name[key] = {
                'quantity': self.individual_value_charges_by_name[key].quantity,
                'value': float("{:.2f}".format(round(value, 2)))
            }
        return total_by_charge_name

    @property
    def total_without_discounts(self):
        """
        Retrieves the totals without any discount on the total value. If the total is less than 0 then it's 0.

        Returns:
            float: The total the user has to pay without discounts
        """
        total = 0
        totals = [value['value'] for value in self.total_by_charge_name.values()]
        if len(totals) > 0:
            total = functools.reduce(lambda x, y: float(x) + float(y), numpy.asarray(totals))
        total = 0 if total < 0 else total
        return total

    @property
    def total(self):
        """
        This gives the total that the company has to pay without discounts. If the total is less than 0 then it's 0.

        Returns:
            float: The total the user has to pay with discounts
        """
        total = self.total_without_discounts
        discount_coupon = float(self.total_coupons_discounts)

        total = (total * discount_coupon['percentage']) - discount_coupon['full']
        total = 0 if total < 0 else total
        return total
