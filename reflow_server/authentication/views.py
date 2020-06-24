from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.authentication.models import UserExtended
from reflow_server.authentication.utils.jwt_auth import JWT
from reflow_server.authentication.serializers import LoginSerializer, UserSerializer, ForgotPasswordSerializer, \
    OnboardingSerializer, ChangePasswordSerializer

from datetime import datetime, timedelta


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    View responsible for authenticating users inside of reflow.
    
    Methods:
        .post() -- authenticate the user based on email and login and returns information about the user as well as 
                   jwt tokens.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            request.user = serializer.save()
            if request.user and request.user.is_authenticated:
                # we also login on session, so the user can see the admin or other pages.
                login(request, request.user)
                
                # get the first form he has access to as the first page to redirect to.
                formulary_service = FormularyService(request.user.id, request.user.company.id)
                first_form_the_user_has_access_to = formulary_service.formulary_names_the_user_has_access_to
                form_name = first_form_the_user_has_access_to[0] if first_form_the_user_has_access_to else ''

                user_serializer = UserSerializer(instance=request.user)

                return Response({
                    'status': 'ok',
                    'company_id': Encrypt.encrypt_pk(request.user.company.id),
                    'form_name': form_name,
                    'user': user_serializer.data,
                    'access_token': JWT.get_token(request.user.id),
                    'refresh_token': JWT.get_refresh_token(request.user.id),
                    'expiration_date': datetime.now() + timedelta(days=180)
                }, status=status.HTTP_200_OK)

        return Response({
            'status': 'error',
            'reason': 'incorrect_pass_or_user'
        }, status=status.HTTP_406_NOT_ACCEPTABLE)


@method_decorator(csrf_exempt, name='dispatch')
class TestTokenView(APIView):
    """
    Simple view just used to validate if a token is still valid or not.
    
    Methods:
        .get() -- we don't validate the token here, we validate using jwt_required() decorator, we just return a ok response
    """
    def get(self, request):
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class ForgotPasswordView(APIView):
    """
    This view uses a temporary password instead of the default password in because of brute force. 
    If a person wants to brute force a password change for all of the emails there will be no changes for users who hasn't requested it.

    The response is always the same independent if it worked or not, so a malicious user can't see which user is valid and which is not valid
    
    Methods:
        .post() -- recieves a json containing the url of the front-end and a email to send a new password 
        and sends a temporary password by email.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class OnboardingView(APIView):
    """
    View that creates a user and a company in the onboarding, this view is responsible 
    for handling only the onbaording

    Methods:
        .post() -- recieves data com user and company and creates a new company
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = OnboardingSerializer(data=request.data)
        if serializer.is_valid():
            if UserExtended.objects.filter(username=serializer.validated_data['user_email']).exists():
                return Response({
                    'status': 'error',
                    'reason': 'existing_user'
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response({
                    'status': 'ok'
                }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'reason': 'invalid_data'
            }, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenView(APIView):
    """
    View that refreshes a token and sends a new token and a new refresh token to the user.

    Methods:
        .get() -- You need to send the refresh token in the header in order to recieve a new token
        and a new refresh token
    """
    def get(self, request):
        jwt = JWT()
        jwt.extract_jwt_from_request(request)
        if jwt.is_valid():
            user = UserExtended.objects.filter(id=jwt.data['id']).first()
            if user and jwt.data['type'] == 'refresh':
                user.last_login = datetime.now()
                user.save()
                return Response({
                    'access_token': JWT.get_token(user.id), 
                    'refresh_token': JWT.get_refresh_token(user.id)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'error',
                    'reason': jwt.invalid_token_error
                }, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({
                'status': 'error',
                'reason': jwt.error
            }, status=status.HTTP_403_FORBIDDEN)


@method_decorator(csrf_exempt, name='dispatch')
class ChangePasswordView(APIView):
    """
    View that recieves a temporary password and a new password and changes the user password to the new password.

    Methods:
        .post() -- Method that recieves the new password and the temp password and changes the user password.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                'status': 'ok'
            }, status=status.HTTP_200_OK)
        
        else:
            return Response({
                'status': 'error',
                'reason': 'invalid_temp_password'
            }, status=status.HTTP_403_FORBIDDEN)
