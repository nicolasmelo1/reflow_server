from django.conf import settings
from django.contrib.auth import authenticate

from rest_framework import serializers
from reflow_server.authentication.managers import api_access_token

from reflow_server.core.events import Event
from reflow_server.authentication.models import UserExtended, Company
from reflow_server.authentication.services.onboarding import OnboardingService
from reflow_server.authentication.services.password import PasswordService
from reflow_server.authentication.services.company import CompanyService
from reflow_server.authentication.utils.jwt_auth import JWT
from reflow_server.authentication.relations import CompanyBillingRelation, APIAccessKeyRelation


class LoginSerializer(serializers.Serializer):
    """
    Serializer responsible for authenticating users in login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def save(self):
        user = authenticate(username=self.validated_data['email'], password=self.validated_data['password'])
        if user:
            Event.register_event('user_login', {
                'user_id': user.id,
                'company_id': user.company_id
            })
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer responsible for retrieving and recieving user data.
    """
    api_access_key = APIAccessKeyRelation(default=False, source='*')

    class Meta:
        model = UserExtended
        exclude = ('password', 'temp_password')


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Simple serializer just used on ForgotPassword View. With this serializer we can send a email to the user if he forgot his password
    it's importat to understand we just use `temp_password` on `reflow_server.authentication.models.UserExtended` model
    since any user can change the password.
    """
    email = serializers.EmailField()
    change_password_url = serializers.CharField()

    def save(self):
        PasswordService.request_new_temporary_password_for_user(self.validated_data['email'], self.validated_data['change_password_url'])


class OnboardingSerializer(serializers.Serializer):
    """
    Serializer that onboards a user and creates a new company and also a new user.
    """
    shared_by = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    partner = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    discount_coupon = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    company_name = serializers.CharField(required=False, allow_blank=True)
    user_phone = serializers.CharField(required=True)
    user_first_name = serializers.CharField(required=True)
    user_last_name = serializers.CharField(required=True)
    user_email = serializers.CharField(required=True)
    user_password = serializers.CharField(required=True)
    user_visitor_id = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def save(self):
        onboarding_service = OnboardingService()
        user = onboarding_service.onboard(
            self.validated_data['user_email'], 
            self.validated_data['user_first_name'], 
            self.validated_data['user_last_name'],
            self.validated_data['user_password'],
            self.validated_data['user_phone'],
            self.validated_data.get('company_name', None),
            self.validated_data.get('shared_by', None),
            self.validated_data.get('partner', None),
            self.validated_data.get('discount_coupon', None),
            self.validated_data.get('user_visitor_id', '')
        )
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer that recieves the user temporary password and the new password and changes the user password.
    """
    temporary_password = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        self.password_service = PasswordService()
        if not self.password_service.isvalid_temporary_password(data['temporary_password']):
            raise serializers.ValidationError(detail={'detail': 'temporary_password', 'reason': 'invalid_temporary_password'})
        return data
    
    def save(self):
        self.password_service.change_password(self.validated_data['password'])


class CompanySerializer(serializers.ModelSerializer):
    """
    This serializer is used for CompanyView. This serializer holds some basic information about the company.
    This way no matter who is using accessing, every user of the company can get this data.
    """
    free_trial_days = serializers.IntegerField(default=settings.FREE_TRIAL_DAYS)
    billing_company = CompanyBillingRelation()
    logo_image_url = serializers.CharField(allow_blank=True, allow_null=True, required=False)

    class Meta:
        model = Company
        fields = ('id', 'endpoint', 'name', 'is_active', 'billing_company', 'logo_image_url', 
                  'free_trial_days', 'created_at')
