from django.db import models

from reflow_server.billing.managers import CompanyChargeBillingManager, PartnerDefaultAndDiscountsBillingManager, \
    DiscountByIndividualNameForCompanyBillingManager, DiscountCouponBillingManager, CompanyCouponsBillingManager


# Create your models here.
class ChargeType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model holds
    the type of what we are charging.

    Right now we can charge the company based on two main variables: USER and COMPANY. First we charge the
    company for the number of users, the type of this charge is __user__ because it's being charged on the user level.
    Okay, but every user on the company might face a limitation on how much they can store in our s3. This is a 
    __company__ charge type because this configuration affect all users inside of a company.

    In the future we can limit how many notifications or how many dashboards a user can have. This can be sometimes
    charged on the user level, or on the company level. So, a company can create n dashboards total, or a user can create
    n dashboards in total inside of this company.
    """
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'charge_type'
        ordering = ('order',)


class ChargeFrequencyType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model holds the frequency
    of the charge. Right now the frequency is only Monthly, but we can add a `yearly` charge in the near future, a `daily`,
    and etc.
    """
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'charge_frequency_type'
        ordering = ('order',)


class InvoiceDateType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model is based just on an interger
    differently from other `type` models. This integer is used for us to know when to charge a company. Some SaaS companies like 
    Spotify or Netflix don't let users select when they want to be charged. Usually they stick to a default date for all of the users,
    others just charge you on the date you joined and started paying.

    We can't work this way since companies have their own unique way of handling expenses. Sometimes the companies recieves the money
    on the end of the month, for others, they prefer to spend on the start of the month. This model holds the possible days they can
    be charged on each month or year.
    """
    date = models.IntegerField()
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'invoice_date_type'
        ordering = ('order',)


class PaymentMethodType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model is for how we charge the user
    it's the payment method. Could be `credit_card`, could be `debit_card`, could be `boleto` and etc.
    """
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'payment_method_type'
        ordering = ('order',)


class IndividualChargeValueType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model holds each individual charge individually.
    For example, each user is 40.00$ and each GB of storage space is 1.00$. These values are when we charge `monthly` only.

    - `default_quantity` is the default quantity of each charge. Like GB of storage space, even though it is 1.00$ for each GB
    of storage space the user cannot have just 1 GB of storage space, these are specified and 'written in stone'.

    With this we can set discounts individually for each charge we make.
    """
    # It doesnt't change frequently
    charge_type = models.ForeignKey('billing.ChargeType', on_delete=models.CASCADE)
    charge_frequency_type = models.ForeignKey('billing.ChargeFrequencyType', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    charge_group_name = models.CharField(max_length=250, blank=True, default='')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    default_quantity = models.IntegerField(null=True, blank=True)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'individual_charge_value_type'
        ordering = ('order',)


# Billing tables
class CompanyBilling(models.Model):
    """
    This model holds the required data for billing. Companies here have a ONE-on-ONE relationship with
    the `authentication.Company` model.

    This data is all the data needed for billing, so it's not something that must exist out of here. If you need any data from here
    in other domains you can add it to Company.
    """
    address = models.CharField(max_length=500, default=None, null=True)
    zip_code = models.CharField(max_length=500, default=None, null=True)
    street = models.CharField(max_length=500, default=None, null=True)
    number = models.IntegerField(null=True)
    neighborhood = models.CharField(max_length=500, default=None, null=True)
    country = models.CharField(max_length=280, default=None, null=True)
    state = models.CharField(max_length=280, default=None, null=True)
    city = models.CharField(max_length=280, default=None, null=True)
    cnpj = models.CharField(max_length=280, default=None, null=True)
    additional_details = models.CharField(max_length=280, default=None, null=True)
    is_supercompany = models.BooleanField(default=False)
    is_paying_company = models.BooleanField(default=False)
    vindi_plan_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_client_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_product_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_payment_profile_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_signature_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    company = models.OneToOneField('authentication.Company', on_delete=models.CASCADE, related_name='billing_company')
    payment_method_type = models.ForeignKey('billing.PaymentMethodType', on_delete=models.CASCADE, null=True)
    charge_frequency_type = models.ForeignKey('billing.ChargeFrequencyType', on_delete=models.CASCADE, null=True)
    invoice_date_type = models.ForeignKey('billing.InvoiceDateType', on_delete=models.CASCADE, null=True)
    
    class Meta:
        db_table = 'company_billing'


class DiscountByIndividualValueQuantity(models.Model):
    """
    This model holds the discounts for each individual charge we make based on quantity. For example on storage space.
    If the user selects 10 Gbs of storage space he recieves 15% discount (so the `value` on this example must be 0.85 because
    we are subtracting 15% of the original value). Then if he selects 20 Gbs of storage space the discount is now 25%, you
    get it.

    Static are discounts that we can give for a lifetime for the user. We do NEVER consider them when calculating the discount
    for a particular quantity, they must be set directly.
    """
    individual_charge_value_type = models.ForeignKey('billing.IndividualChargeValueType', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=250)

    class Meta:
        db_table = 'discount_by_individual_value_quantity'


class PartnerDefaultAndDiscounts(models.Model):
    """
    If a company has come from a partner we use the partner defaults. With this we can set the discount value by each 
    `individual_charge_value_type` we want to give discounts and also we can set a default quantity for each funcionality 
    of our platform for the user.

    IMPORTANT: notice that partner_name must comply with reflow_server.authentication.models.Company partner attribute.
    """
    partner_name = models.CharField(max_length=200)
    individual_charge_value_type = models.ForeignKey('billing.IndividualChargeValueType', on_delete=models.CASCADE)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    default_quantity = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'partner_default_and_discounts'

    billing_ = PartnerDefaultAndDiscountsBillingManager()


class DiscountByIndividualNameForCompany(models.Model):
    """
    This model is responsible for holding the discounts for each billing.IndividualChargeValueType but the difference here
    is that they are not based on quantity like `reflow_server.billing.models.DiscountByIndividualValueQuantity` but for each company
    directly. 

    The above automatically checks if a company has a discount for a specific `reflow_server.billing.models.IndividualChargeValueType`.
    """
    individual_charge_value_type = models.ForeignKey('billing.IndividualChargeValueType', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=250)
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE)

    class Meta:
        db_table = 'discount_by_individual_name_for_company'

    objects = models.Manager()
    billing_ = DiscountByIndividualNameForCompanyBillingManager()


class DiscountCoupon(models.Model):
    """
    The model `reflow_server.billing.models.DiscountByIndividualValueQuantity` are discounts we define internally as a company,
    Discount coupon is coupons we can give to the user so he can have a certain discount on his invoice.

    Discount Coupons are usually not for the lifetime, we need a start_date and an end_date. Sometimes they can be permanent,
    but only sometimes (like for collaborators of reflow for example).
    """
    name = models.CharField(max_length=250, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    permanent = models.BooleanField(default=False)
    start_at = models.DateTimeField(null=True, default=None)
    end_at = models.DateTimeField(null=True, default=None)
    
    class Meta:
        db_table = 'discount_coupon'

    billing_ = DiscountCouponBillingManager()


class CompanyCoupons(models.Model):
    """
    A company can have more than one discount coupon at the same time, we store this in this model. So we can control
    what discounts from coupons we will give him.
    """
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, related_name='company_discount_coupons')
    discount_coupon = models.ForeignKey(DiscountCoupon, on_delete=models.CASCADE)

    class Meta:
        db_table = 'company_coupon'

    billing_ = CompanyCouponsBillingManager()

class CompanyInvoiceMails(models.Model):
    """
    Simple model that holds the emails that will recieve the invoice of the company. It's important to understand that
    here email are just strings. This happens because the finance team doesn't need to be a user in our system.
    """
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, related_name='company_invoice_emails')
    email = models.EmailField(max_length=254)

    class Meta:
        db_table = 'company_invoice_mails'
        ordering = ('id',)

class CurrentCompanyCharge(models.Model):
    """
    This model holds the current charge for a company. We usually use this model to make the calculation on how much we
    should charge of the company on each month. 

    This is also the model that is updated whenever a user updates some billing information. This is because this model holds
    static values. There are no dates attached to this model (excepted created_at and updated_at used for analytics) so this does
    not refresh on every payment, it's not how this works.

    To understand how we bill for dashboard charts go to: reflow_server.dashboard.services.permissions.DashboardPermissionsService
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, related_name='current_company_charges')
    individual_charge_value_type = models.ForeignKey('billing.IndividualChargeValueType', on_delete=models.CASCADE)
    discount_by_individual_value = models.ForeignKey('billing.DiscountByIndividualValueQuantity', on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'current_company_charge'


class CompanyCharge(models.Model):
    """
    The charge of the company, this is after a payment has been made, this is used for analytics. Right now Vindi handles 
    all of the payments, this is updated when our webhook recieves that a payment has been made for a company.
    """
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    attempt_count = models.IntegerField(default=0)
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, related_name='company_charges')

    class Meta:
        db_table = 'company_charge'

    objects = models.Manager()
    billing_ = CompanyChargeBillingManager()