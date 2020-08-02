from django.contrib.auth import authenticate

from rest_framework import serializers

from reflow_server.authentication.models import UserExtended, Company, ProfileType
from reflow_server.authentication.services.onboarding import OnboardingService
from reflow_server.authentication.services.password import PasswordService
from reflow_server.authentication.utils.jwt_auth import JWT

import unicodedata


class LoginSerializer(serializers.Serializer):
    """
    Serializer responsible for authenticating users in login.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def save(self):
        user = authenticate(username=self.validated_data['email'], password=self.validated_data['password'])
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer responsible for retrieving and recieving user data.
    """
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
    company_name = serializers.CharField(required=False, allow_blank=True)
    user_phone = serializers.CharField(required=True)
    user_first_name = serializers.CharField(required=True)
    user_last_name = serializers.CharField(required=True)
    user_email = serializers.CharField(required=True)
    user_password = serializers.CharField(required=True)

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
            self.validated_data.get('partner', None)
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
            raise serializers.ValidationError()
        return data
    
    def save(self):
        self.password_service.change_password(self.validated_data['password'])


class CompanySettingsSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = Company
        fields = ('name',) 