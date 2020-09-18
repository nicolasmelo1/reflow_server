from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from reflow_server.authentication.managers import UserExtendedAuthenticationManager, \
    CompanyAuthenticationManager
from reflow_server.billing.managers import UserExtendedBillingManager, CompanyBillingManager, \
    AddressHelperBillingManager
from reflow_server.data.managers import UserExtendedDataManager
from reflow_server.formulary.managers import UserExtendedFormularyManager
from reflow_server.notification.managers import UserExtendedNotificationManager
from reflow_server.theme.managers import UserExtendedThemeManager


class VisualizationType(models.Model):
    name = models.CharField(max_length=250)
    label_name = models.CharField(max_length=200)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'data_type'
        ordering = ('order',)


class CompanyType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. It defines the type
    of the company, company types defines which service the company is in:
    could be `industry`, could be a `startup`, could be `Information and Technology Services` you get it.
    """
    name = models.CharField(max_length=200)
    label_name = models.CharField(max_length=200, null=True, blank=True)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'company_type'
        ordering = ('order',)


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
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'profiles'
        ordering = ('order',)


class AddressHelper(models.Model):
    """
    This model is a `helper` so it contains data used that is used but is not required. Usually this
    type of model offers an ammount of data but doesn't relate directly to any table in the database 
    (They are not used as ForeignKeys).
    It defines the address options for the user so we will have all of the cities from every state from 
    every country we support.
    """
    country_code = models.CharField(max_length=50)
    country_name = models.CharField(max_length=200)
    state = models.CharField(max_length=400)
    state_code = models.CharField(max_length=100)
    city = models.CharField(max_length=400)
    order = models.BigIntegerField(default=1)
    
    class Meta:
        db_table = 'address_helper'
        ordering = ('order',)

    objects = models.Manager()
    billing_ = AddressHelperBillingManager()


class Company(models.Model):
    """
    This is the company, the company as the name suggest is the company of a user, right now a user can have only one
    company, but might change in the future for a user to have multiple companies.

    A Company defines everything on a company level. Stuff like payment info, stuff to send "Nota fiscal" and others
    MUST NOT be defined here, they are defined on `reflow_server.billing.models.CompanyBilling` model since this is data
    needed only for billing and not for here.
    """
    name = models.CharField(max_length=400, default=None, db_index=True)
    endpoint = models.CharField(max_length=280, default=None, db_index=True)
    company_type = models.ForeignKey('authentication.CompanyType', on_delete=models.CASCADE, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)
    shared_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    partner = models.CharField(max_length=500, default=None, null=True, blank=True)
    logo_image_bucket = models.CharField(max_length=200, default=settings.S3_BUCKET)
    logo_image_path = models.CharField(max_length=250, default=settings.S3_COMPANY_LOGO_PATH)
    logo_image_url = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'company'

    objects = models.Manager()
    authentication_ = CompanyAuthenticationManager()
    billing_ = CompanyBillingManager()


class UserExtended(AbstractUser):
    """
    This is the user model, as you can see it doesn't inherit directly from models.Model but from AbstractUser.

    So what happens is, Django is tightly coupled with the `users` model. Also the default users model already solves
    most of the common security vulnerabilities we might face. This way it is easier for us to just extend the default
    `user` model.

    This model defines stuff we might want to have on a `user` level. We define stuff like company, profile, if the user is
    an admin (this admin is the admin that can access the default django url /admin, not the profile admin) or not, and etc.
    """
    company = models.ForeignKey('authentication.Company', on_delete=models.CASCADE, default=None)
    profile = models.ForeignKey('authentication.ProfileType', on_delete=models.CASCADE, default=None)
    phone = models.CharField(max_length=250, default=None, null=True, blank=True)
    timezone = models.IntegerField(default=-3)
    is_admin = models.BooleanField(default=False)
    data_type = models.ForeignKey('authentication.VisualizationType', on_delete=models.CASCADE, default=None, null=True)
    temp_password = models.CharField(max_length=250, default=None, null=True, blank=True)
    
    class Meta:
        db_table = 'users'

    objects = models.Manager()
    authentication_ = UserExtendedAuthenticationManager()
    billing_ = UserExtendedBillingManager()
    data_ = UserExtendedDataManager()
    formulary_ = UserExtendedFormularyManager()
    notification_ = UserExtendedNotificationManager()
    theme_ = UserExtendedThemeManager()
    
    def make_temporary_password(self):
        from reflow_server.authentication.utils.jwt_auth import JWT
        
        password = JWT.get_token(self.id)
        self.temp_password = password
        self.save()
        return password