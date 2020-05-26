from django.db import models
from django.contrib.auth.models import AbstractUser



class CompanyType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. It defines the type
    of the company, company types defines which service the company is in:
    could be `industry`, could be a `startup`, could be `Information and Technology Services` you get it.
    """
    name = models.CharField(max_length=200)
    label_name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'company_type'
        ordering = ('id',)


class ProfileType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model defines
    a type of profile, each profile change what the user can see, and what a user has access to.
    - If a user is an `simple_user`: he only have access on what he insert in the system, also, on the filters 
    defined on `formulary.models.OptionAccessedBy` and `formulary.models.FormAccessedBy` that applies to him.
    - If a user is an `coordinator`: He have access on what other users have inserted in the system, also, 
    on the filters defined on `formulary.models.OptionAccessedBy` and `formulary.models.FormAccessedBy` that applies to him.
    - If a user is an `admin`: he have access to some admin urls, and have access to most of the data, also, 
    on the filters defined on `formulary.models.OptionAccessedBy` and `formulary.models.FormAccessedBy` that applies to him.
    """
    name = models.CharField(max_length=200)
    label_name = models.CharField(max_length=200, null=True, blank=True)
    can_edit = models.BooleanField(default=False)

    class Meta:
        db_table = 'profiles'


class Company(models.Model):
    """
    This is the company, the company as the name suggest is the company of a user, right now a user can have only one
    company, but might change in the future for a user to have multiple companies.

    A Company defines everything on a company level. So stuff like payment info, stuff to send "Nota fiscal" and others
    MUST be defined here, not on the user level.
    """
    name = models.CharField(max_length=400, default=None, db_index=True)
    endpoint = models.CharField(max_length=280, default=None, db_index=True)
    company_type = models.ForeignKey('auth.CompanyType', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=500, default=None, null=True)
    zip_code = models.CharField(max_length=500, default=None, null=True)
    street = models.CharField(max_length=500, default=None, null=True)
    number = models.IntegerField(null=True)
    neighborhood = models.CharField(max_length=500, default=None, null=True)
    country = models.CharField(max_length=280, default=None, null=True)
    state = models.CharField(max_length=280, default=None, null=True)
    city = models.CharField(max_length=280, default=None, null=True)
    cnpj = models.CharField(max_length=280, default=None, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_supercompany = models.BooleanField(default=False)
    is_paying_company = models.BooleanField(default=False)
    vindi_plan_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_client_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_product_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_payment_profile_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    vindi_signature_id = models.CharField(max_length=280, default=None, null=True, db_index=True)
    shared_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    partner = models.CharField(max_length=500, default=None, null=True, blank=True)
    payment_method_type = models.ForeignKey('billing.PaymentMethodType', on_delete=models.CASCADE, null=True)
    charge_frequency_type = models.ForeignKey('billing.ChargeFrequencyType', on_delete=models.CASCADE, null=True)
    invoice_date_type = models.ForeignKey('billing.InvoiceDateType', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'company'


class UserExtended(AbstractUser):
    """
    This is the user model, as you can see it doesn't inherit directly from models.Model but from AbstractUser.

    So what happens is, Django is tightly coupled with the `users` model. Also the default users model already solves
    most of the common security vulnerabilities we might face. This way it is easier for us to just extend the default
    `user` model.

    This model defines stuff we might want to have on a `user` level. We define stuff like company, profile, if the user is
    an admin (this admin is the admin that can access the default django url /admin, not the profile admin) or not, and etc.
    """
    company = models.ForeignKey('auth.Company', on_delete=models.CASCADE, default=None)
    profile = models.ForeignKey('auth.ProfileType', on_delete=models.CASCADE, default=None)
    phone = models.CharField(max_length=250, default=None, null=True, blank=True)
    timezone = models.IntegerField(default=-3)
    is_admin = models.BooleanField(default=False)
    data_type = models.ForeignKey('visualization.DataType', on_delete=models.CASCADE, default=None, null=True)
    temp_password = models.CharField(max_length=250, default=None, null=True, blank=True)
    
    class Meta:
        db_table = 'users'

    def make_temporary_password(self):
        from reflow_server.auth.utils.jwt_auth import JWT
        
        password = JWT.get_token(self.id)
        self.temp_password = password
        self.save()
        return password