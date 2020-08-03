from django.db import transaction
from django.db.models import Q

from reflow_server.authentication.models import UserExtended
from reflow_server.billing.models import CurrentCompanyCharge, DiscountByIndividualValue, \
    IndividualChargeValueType, ChargeType
from reflow_server.billing.services.data import TotalData
from reflow_server.billing.services.vindi import VindiService


class ChargeService:
    def __init__(self, company):
        """
        This service is responsible for handling each charge of a specific company. Billing is
        usually separated by 
        - The Payment Information: What is the user credit card, who we will mail on the invoice, when 
                                   the user will be charged and other informations.
        - The Charge information: It's how much we will bill the user for each funcionality we offer.
        
        This service handles the Charge information.

        Args:
            company (reflow_server.authentication.models.Company): Which company are we charging, send the object directly.
        """
        self.company = company

    def push_updates(self):
        """
        Sends the updates made here in our billing service to our Payment Gateway, so the Payment
        Gateway can work with new data.
        """
        if self.company.is_paying_company:
            vindi_service = VindiService(self.company.id)
            vindi_service.create_or_update()
    
    def remove_charge_values_from_removed_users(self):
        """
        Removes all of the CurrentCompanyCharges that are bound to a removed user. Obviously, doesn't consider the ones that are for the
        company, so with user_id set to None
        """
        company_users = UserExtended.objects.filter(company_id=self.company.id, is_active=True)
        CurrentCompanyCharge.objects.filter(company_id=self.company.id).exclude(Q(user_id__isnull=True) | Q(user_id__in=company_users)).delete()
        return True

    def remove(self, charge_value_name, user_id=None, push_updates=True):
        """
        Removes a charge from the company based on the charge_value_name of this charge, this way you can remove users, storage capacity and other 
        charge data.

        Args:
           charge_value_names (str): A string containing the name of a single individual_charge_type to be removed
                                     for this particular company. Check reflow_server.billing.models.IndividualChargeValueType 
                                     table in our database for the possible values.
            user_id (int, optional): The id of the user, this is only required when changing individualChargeValueType that is based
                                     on the user, not the company itself. Defaults to None.
            push_updates (bool, optional): set this to True if you want to push this update to our payment gateway. 
                                           If set to false it saves in our database but doesn't update the payment gateway with the
                                           new information. Defaults to True
        """
        if user_id:
            to_delete = CurrentCompanyCharge.objects.filter(company_id=self.company.id, user_id=user_id, individual_charge_value_type__name=charge_value_name)
        else:
            to_delete = CurrentCompanyCharge.objects.filter(company_id=self.company.id, user__isnull=True, individual_charge_value_type__name=charge_value_name)
        if to_delete:
            to_delete.delete()
            if push_updates:
                self.push_updates()
            return True
        else:
            return False

    def create(self, charge_value_names, user_id=None, push_updates=True):
        """
        Creates a new charge for the company for a particular individual_charge_type. Could be a new user being
        created, a new storage capacity or a new dashboard for the company and so on.

        Args:
            charge_value_names (list): A list containing the names of each individual_charge_type to be created
                                       for this particular company. Check reflow_server.billing.models.IndividualChargeValueType 
                                       for reference
            user_id (int, optional): The id of the user, this is only required when changing individualChargeValueType that is based
                                     on the user, not the company itself. Defaults to None.
            push_updates (bool, optional): set this to True if you want to push this update to our payment gateway. 
                                           If set to false it saves in our database but doesn't update the payment gateway with the
                                           new information. Defaults to True

        Returns:
            list: list of reflow_server.billing.models.CurrentCompanyCharge, returns each model that was created in the database.
        """
        created = list()
        for charge_value_name in charge_value_names:
            created.append(
                self.update_or_create(charge_value_name, user_id=user_id, push_updates=push_updates)
            )
        return created

    def get_total_data_from_custom_charge_quantity(self, current_company_charges):
        """
        Gets the totals based on a custom value that is not saved in our database. We usually need and use this so the user can have 
        a feedback while changing the quantity values while updating the billing information.

        Args:
            individual_charge_value_types (list(reflow_server.billing.services.data.CompanyChargeData)): The list of charges for this function
                                                                                                         to calculate
        Returns:
            reflow_server.billing.services.data.TotalData: Totals object with handy functions.
        """
        total_data = TotalData(company_id=self.company.id)
        for company_charge in current_company_charges:
            individual_charge_value = IndividualChargeValueType.objects.filter(name=company_charge.charge_name).first()
            if individual_charge_value:
                discount = self.__get_discount(individual_charge_value.id, company_charge.quantity)
                value = individual_charge_value.value
                discount_percentage = discount.value if discount else 1
                quantity = company_charge.quantity
                total_data.add_value(company_charge.charge_name, value, quantity, discount_percentage)
        return total_data

    @property
    def get_total_data(self):
        """
        Returns a TotalData object, this object is a handy object for retriving totals in many possible ways.
        You can retrieve the totals in the most simple way, but this object also can retrieve totals from each 
        individual charge name, discounts, coupon discounts and so on. That's why it's preferrable to retrieve 
        an object in this case instead of a simple value.

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
        """
        Gets the discount for a particular individual_charge_value_type and based on a specific quantity.

        Args:
            individual_charge_value_type_id (int): The id of the individual_charge_value
            quantity (int): the quantity of this particular individual charge

        Returns:
            reflow_server.billing.models.DiscountByIndividualValue: The discount object to consider.
        """
        return DiscountByIndividualValue.objects.filter(
            individual_charge_value_type_id=individual_charge_value_type_id, 
            quantity__lte=quantity,
            static=False
        ).order_by('-quantity').first()

    @transaction.atomic
    def update_or_create(self, charge_value_name, user_id=None, quantity=None, push_updates=True):
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