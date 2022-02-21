from django.db import transaction

from reflow_server.authentication.models import UserExtended, Company
from reflow_server.billing.models import BillingPlanPermission, CurrentCompanyCharge, DiscountByIndividualValueQuantity, \
    IndividualChargeValueType, DiscountByIndividualNameForCompany, CompanyCharge, \
    CompanyBilling, PartnerDefaultAndDiscounts, CompanyChargeSent
from reflow_server.billing.services.data import TotalData, CompanyChargeData
from reflow_server.billing.services.vindi import VindiService

from datetime import datetime, timedelta


class ChargeService:
    def __init__(self, company_id, company_billing):
        """
        This service is responsible for handling each charge of a specific company. Billing is
        usually separated by 
        - The Payment Information: What is the user credit card, who we will mail on the invoice, when 
                                   the user will be charged and other informations.
        - The Charge information: It's how much we will bill the user for each funcionality we offer.
        
        This service handles the Charge information.

        Args:
            company (int): The company_id we are changing
            company_billing (reflow_server.billing.models.CompanyBilling): This is a CompanyBilling instance, 
                                                                           it is similar to Company but holds all
                                                                           of the billing data for a particular company
        """
        self.company_id = company_id
        self.company_billing = company_billing

    def push_updates(self):
        """
        Sends the updates made here in our billing service to our Payment Gateway, so the Payment
        Gateway can work with new data.
        """
        if not self.company_billing.is_supercompany and self.company_billing.is_paying_company:
            vindi_service = VindiService(self.company_id)
            vindi_service.create_or_update()

    def validate_current_company_charges_and_create_new(self, current_company_charges):
        """
        This is used for two things, it validates the current_company_charges. So if the user access directly the API and tries to not add
        a company charge we will automatically add it for him guaranteeing that all of the existing IndividualValueChargeType are created
        for a specific company. The nice thing to this is that automatically we can add the CurrentCompanyCharge data, so by
        sending an empty list you will end up with the actual `current_company_charges` list with `reflow_server.billing.services.data.CompanyChargeData`
        objects to be used when saving the data or retrieving the totals.

        Important:
        You will notice we always consider 'per_user' was not added, this is because we can prevent the user for setting any value for this special case
        and set it directly here on the backend.

        IMPORTANT:
        If a current_company_charge instance exists for a particular individual_charge_value_type we will use this quantity instead of the individual_charge_value_type
        default quantity

        Args:
            current_company_charges (list(reflow_server.billing.services.data.CompanyChargeData)): List of CompanyChargeData to verify and check if is complete
            if any `IndividualValueChargeType` is left out, we actually add it to the list. 

        Returns:
            list(reflow_server.billing.services.data.CompanyChargeData): returns the new list of `CompanyChargeData` objects
            to be used when saving or retrieivng totals
        """
        # first we need to filter all of the current_company_charge that are not 'per_user' and then we need to add only
        # the individual_charge_value_type_name to the existing_company_charge_names list so we  get the individual_charges
        # that we need to add
        new_curent_company_charges = []
        existing_company_charge_names = []
        for current_company_charge in current_company_charges:
            if current_company_charge.individual_value_charge_name != 'per_user' and current_company_charge.quantity != None:
                new_curent_company_charges.append(current_company_charge)
                existing_company_charge_names.append(current_company_charge.individual_value_charge_name)
        individual_charges_to_add = IndividualChargeValueType.objects.exclude(name__in=existing_company_charge_names)

        for individual_charge_value_type in individual_charges_to_add:
            current_company_charge = CurrentCompanyCharge.objects.filter(individual_charge_value_type=individual_charge_value_type, company_id=self.company_id).first()
            quantity = individual_charge_value_type.default_quantity
            if current_company_charge:
                quantity = current_company_charge.quantity
            # when it's per_user we always count the number of active users in the company
            if individual_charge_value_type.name == 'per_user':
                quantity = UserExtended.billing_.users_active_by_company_id(company_id=self.company_id).count() 
            new_curent_company_charges.append(CompanyChargeData(individual_charge_value_type.id, quantity))

        return new_curent_company_charges
        
    def get_total_data_from_custom_charge_quantity(self, plan_id, current_company_charges=[]):
        """
        Gets the totals based on a custom value that is not saved in our database. We usually need and use this so the user can have 
        a feedback while changing the quantity values while updating the billing information.

        If you set the current_company_charges as and empty list we will create a fresh TotalData

        Args:
            plan_id (int): The id of the plan selected by the user.
            individual_charge_value_types (list(reflow_server.billing.services.data.CompanyChargeData)): The list of charges for this function
                                                                                                         to calculate. If set to empty we will retrieve
                                                                                                         a fresh TotalData fully validated, respecting the existing data.
                                                                                                         Defaults to []
        Returns:
            reflow_server.billing.services.data.TotalData: Totals object with handy functions.
        """
        total_data = TotalData(company_id=self.company_id)
        current_company_charges = self.validate_current_company_charges_and_create_new(current_company_charges)
        for company_charge in current_company_charges:
            individual_charge_value = IndividualChargeValueType.objects.filter(name=company_charge.individual_value_charge_name).first()
            plan_increase = BillingPlanPermission.billing_.plan_increase_by_plan_id_and_individual_charge_value_type_id(
                plan_id,
                individual_charge_value.id
            )

            if individual_charge_value:
                discount_from_quantity = self.get_discount_for_quantity(plan_id, individual_charge_value.id, company_charge.quantity)
                discount_from_quantity = discount_from_quantity.value if discount_from_quantity else 1
                
                discount_by_individual_charge_type_for_company = self.__get_discount_for_company_from_a_individual_charge_value_type(individual_charge_value.id)
                discount_by_individual_charge_type_for_company = discount_by_individual_charge_type_for_company.value \
                    if discount_by_individual_charge_type_for_company else 1

                discount_percentage = discount_from_quantity * discount_by_individual_charge_type_for_company
                value = individual_charge_value.value
                quantity = company_charge.quantity
                plan_increase = plan_increase if plan_increase != None else 1
                
                total_data.add_value(
                    company_charge.individual_value_charge_name, 
                    company_charge.charge_type_name, 
                    value, 
                    quantity, 
                    discount_percentage,
                    plan_increase
                )
        return total_data
    
    def __get_discount_for_company_from_a_individual_charge_value_type(self, individual_charge_value_type_id):
        """
        Sometimes we can give discounts for a spcefic company for a especifically funcionality on the plataform. The quantity one 
        always works for every client on the platform. With this one we can set special discounts for companies and each funcionality.
        """
        return DiscountByIndividualNameForCompany.objects.filter(
            company_id=self.company_id, 
            individual_charge_value_type_id=individual_charge_value_type_id
        ).first()

    def get_discount_for_quantity(self, plan_id, individual_charge_value_type_id, quantity):
        """
        Gets the discount for a particular individual_charge_value_type and based on a specific quantity.

        Args:
            plan_id (int): The id of the plan selected by the user.
            individual_charge_value_type_id (int): The id of the individual_charge_value
            quantity (int): the quantity of this particular individual charge

        Returns:
            reflow_server.billing.models.DiscountByIndividualValueQuantity: The discount object to consider.
        """
        return DiscountByIndividualValueQuantity.objects.filter(
            plan_id=plan_id,
            individual_charge_value_type_id=individual_charge_value_type_id, 
            quantity__lte=quantity
        ).order_by('-quantity').first()

    @transaction.atomic
    def update_or_create(self, charge_value_name, quantity=None, push_updates=True):
        """
        This updates or creates a specific reflow_server.billing.models.CurrentCompanyCharge in our database. This model
        is responsible for holding the current state of our payment, it's how much we must charge right now on this exact moment even if we are not 
        charging the company right now.

        Args:
            charge_value_name (str): You always update a unique and specific IndividualChargeValueType name. 
                                     You can check the possible options in our database.
            quantity (int, optional): The quantity of the items that you are trying to update, it's like putting fruits in a basket. Defaults to None.
            push_updates (bool, optional): Set to False if you don't want to push the updates to our Payment Gateway. Defaults to True.

        Raises:
            AssertionError: If you are trying to update a `user` ChargeType but you do not send a `user_id` parameter
            KeyError: raised when passing a wrong `charge_value_name` parameter, raises the possible options.

        Returns:
            reflow_server.billing.models.CurrentCompanyCharge: The added or updated CurrentCompanyCharge.
        """
        individual_charge_value_type = IndividualChargeValueType.objects.filter(name=charge_value_name).first()
        
        if not individual_charge_value_type:
            raise KeyError(
                'Your `charge_value_name` parameter must be one of the following options: {}'.format(
                    ', '.join(list(IndividualChargeValueType.objects.all().values_list('name', flat=True)))
                )
            )
        
        # if quantity is not defined we use the quantity of the default quantity defined in IndividualChargeValueType
        if not quantity:
            company = Company.billing_.company_by_company_id(self.company_id)
            partner_default_and_discounts = PartnerDefaultAndDiscounts.billing_.partner_default_and_discount_by_partner_name_and_individual_charge_value_type_id(
                company.partner,
                individual_charge_value_type.id
            )
            # If partner defaults exists and a default quantity is set use it, otherwise use the default quantity of the individual
            # charge value
            if partner_default_and_discounts and partner_default_and_discounts.default_quantity != None:
                quantity = partner_default_and_discounts.default_quantity
            else:
                quantity = individual_charge_value_type.default_quantity

        discount = self.get_discount_for_quantity(self.company_billing.plan_id, individual_charge_value_type.id, quantity)
        
        charge_instance, __ = CurrentCompanyCharge.objects.update_or_create(
            individual_charge_value_type=individual_charge_value_type, 
            company_id=self.company_id, 
            defaults={
                'discount_by_individual_value': discount,
                'quantity': quantity
        })

        if push_updates:
            self.push_updates()
        return charge_instance

    @staticmethod
    def add_new_company_charge(company_id, total_value, attempt_count):
        """
        This static function is responsible for saving to our database that the user has made a payment for a invoice.
        This is nice for us so we can keep track of all of the payments made by the user in our platform, we can easily spot frauds
        and other stuff with it.

        We also prevent updates in less than a minute, so two requests being fired at the same time doesn't save twice.

        Args:
            company_id (int): the company_id that made the payment.
            total_value (float): The amout the user has paid
            attempt_count (int): how many attempts we needed to bill the user.
        """
        today_end = datetime.now()
        today_start = today_end - timedelta(minutes=1)
        company_charges_updated_in_the_last_minute = CompanyCharge.billing_.exists_company_charge_created_between_dates_by_company(
            company_id=company_id, date_end=today_end, date_start=today_start
        )
        if not company_charges_updated_in_the_last_minute:
            CompanyCharge.billing_.create_company_charge(
                company_id=company_id,
                total_value=total_value,
                attempt_count=attempt_count
            )
        return True

    
    @staticmethod
    def add_new_company_charge_sent(vindi_customer_id, total_value):
        """
        When the vindi charge is sent to the user we update here, this is only used for analytics purpose, it does not serve anything inside of the application.
        This way we can have analytics like: understand the number of user that we billed for each month and then compare by the paid.

        Args:
            vindi_customer_id (str): The vindi client id. This is a string although the string is a number
            total_value (float): The amout the user needs to pay
        """
        company_billing = CompanyBilling.objects.filter(vindi_client_id=vindi_customer_id).first()
        if company_billing:
            CompanyChargeSent.billing_.create_company_charge_sent(
                company_id=company_billing.company_id,
                total_value=total_value,
            )