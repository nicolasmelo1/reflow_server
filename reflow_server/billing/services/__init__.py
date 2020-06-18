from django.db import transaction

from reflow_server.authentication.models import Company
from reflow_server.billing.models import ChargeType, IndividualChargeValueType, DiscountByIndividualValue, \
    CurrentCompanyCharge
from reflow_server.billing.services.data import TotalData

    
class BillingService:
    """
    Helper for change company charges without much difficulty inside the code.
    Also it is used to check permissions by billing

    it recieves a company_id to instantiate the class and make the changes accordingly
    """
    def __init__(self, company_id):
        self.company = Company.objects.filter(id=company_id).first()

    @property
    def get_total_data(self):
        """
        Returns a TotalData object, this object is a handy object for retriving totals in many possible ways.
        You can retrieve the totals in the most simple way, but this object also can retrieve totals from each individual charge name, discounts, coupon discounts
        and so on. That's why it's preferrable to retrieve an object in this case instead of a simple value.

        Returns:
            reflow_server.billing.services.data.TotalData: Object with handy functions.
        """
        total_data = TotalData(company_id=self.company.id)
        for current_company_charge in CurrentCompanyCharge.objects.filter(company=self.company):
            value = current_company_charge.individual_charge_value_type.value
            discount_percentage = current_company_charge.discount_by_individual_value.value if current_company_charge.discount_by_individual_value else 1
            quantity = current_company_charge.quantity
            total_data.add_value(current_company_charge.individual_charge_value_type.name, value, quantity, discount_percentage)

        return total_data

    def __get_discount(self, individual_charge_value_type_id, quantity):
        return DiscountByIndividualValue.objects.filter(
            individual_charge_value_type_id=individual_charge_value_type_id, 
            quantity__lte=quantity
        ).order_by('-quantity').first()

    def push_updates(self):
        if self.company.is_paying_company:
            pass

    @transaction.atomic
    def update(self, charge_value_name, user_id=None, quantity=None, push_updates=True):
        """
        This updates or creates a specific reflow_server.billing.models.CurrentCompanyCharge in our database. This model
        is responsible for holding the current state of our payment, it's how much we must charge right now on this exact moment even if we are not 
        charging the company right now.

        Args:
            charge_value_name (str): You always update a unique and specific IndividualChargeValueType name. 
                                     You can check the possible options in our database.
            user_id (int, optional): If you are updating the charge of a specific user you must set the user_id, refer to ChargeType. Defaults to None.
            quantity (int, optional): The quantity of the items that you are trying to update, it's like putting fruits in a basket. Defaults to None.
            push_updates (bool, optional): Set to False if you don't want to push the updates to our Payment Gateway. Defaults to True.

        Raises:
            AssertionError: If you are trying to update a `user` ChargeType but you do not send a `user_id` parameter
            KeyError: raised when passing a wrong `charge_value_name` parameter, raises the possible options.

        Returns:
            reflow_server.billing.models.CurrentCompanyCharge: The added or updated CurrentCompanyCharge.
        """
        charge_type = ChargeType.objects.filter(name='user' if user_id else 'company').first()
        individual_charge_value_type = IndividualChargeValueType.objects.filter(name=charge_value_name, charge_type=charge_type).first()
        
        if not individual_charge_value_type:
            if IndividualChargeValueType.objects.filter(name=charge_value_name, charge_type__name='user').exists():
                raise AssertionError('`user_id` parameter is obligatory for the `{}` charge value name'.format(charge_value_name))
            else:
                raise KeyError(
                    'Your `charge_value_name` parameter must be one of the following options: {}'.format(
                        ', '.join(list(IndividualChargeValueType.objects.all().values_list('name', flat=True)))
                    )
                )
        
        # if quantity is not defined we use the quantity of the default quantity defined in IndividualChargeValueType
        if not quantity:
            quantity = individual_charge_value_type.default_quantity

        discount = self.__get_discount(individual_charge_value_type.id, quantity)
        
        charge_instance, __ = CurrentCompanyCharge.objects.update_or_create(
            individual_charge_value_type=individual_charge_value_type, 
            company=self.company, 
            user_id=user_id,
            defaults={
                'discount_by_individual_value': discount,
                'quantity': quantity
        })

        if push_updates:
            self.push_updates()
        return charge_instance

    def remove_user(self, user_id):
        CurrentCompanyCharge.objects.filter(company=self.company, user_id=user_id).delete()
        return True

    def __create(self, charge_value_names, push_updates, user_id=None):
        updated = list()
        for charge_value_name in charge_value_names:
            updated.append(
                self.update(charge_value_name, user_id=user_id, push_updates=push_updates)
            )
        return updated

    @transaction.atomic
    def create_user(self, user_id, push_updates=True):
        """
        Used for when creating a new user only, when updating you should use `.update()` method directly.
        It just loops for each 'charge_value_names' passing only the name as parameter, this way we always force to use the defauld value.

        Args:
            push_updates (bool, optional): Set to False if you don't want to push the updates to our Payment Gateway. Defaults to True.

        Returns:
            list(reflow_server.billing.models.CurrentCompanyCharge): This data is a list of the instances of the newly created CurrentCompanyCharge.
                                                                     each item on the list represents each row inserted on the database.
        """
        charge_value_names = ['per_user']

        return self.__create(charge_value_names, user_id=user_id, push_updates=push_updates)

    @transaction.atomic
    def create_company(self, push_updates=True):
        """
        Used for when creating a new company only, when updating you should use `.update()` method directly.
        It just loops for each 'charge_value_names' passing only the name as parameter, this way we always force to use the defauld value.

        Args:
            push_updates (bool, optional): Set to False if you don't want to push the updates to our Payment Gateway. Defaults to True.

        Returns:
            list(reflow_server.billing.models.CurrentCompanyCharge): This data is a list of the instances of the newly created CurrentCompanyCharge.
                                                                     each item on the list represents each row inserted on the database.
        """
        charge_value_names = ['per_gb']

        return self.__create(charge_value_names, push_updates=push_updates)


    @classmethod
    @transaction.atomic
    def create_on_onboarding(cls, company_id, user_id):
        billing_service = cls(company_id)
        billing_service.create_company(push_updates=False)
        billing_service.create_user(user_id=user_id, push_updates=False)
        billing_service.push_updates()
        return True
    

