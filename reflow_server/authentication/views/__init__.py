from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from reflow_server.core.utils.encrypt import Encrypt
from reflow_server.core.utils.csrf_exempt import CsrfExemptSessionAuthentication
from reflow_server.formulary.services.formulary import FormularyService
from reflow_server.authentication.services.users import UsersService
from reflow_server.authentication.models import UserExtended, Company
from reflow_server.authentication.utils.jwt_auth import JWT
from reflow_server.authentication.serializers import LoginSerializer, UserSerializer, ForgotPasswordSerializer, \
    OnboardingSerializer, ChangePasswordSerializer, CompanySerializer

from datetime import datetime, timedelta


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    """
    View responsible for authenticating users inside of reflow.
    
    Methods:
        POST: authenticate the user based on email and login and returns information about the user as well as 
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

                user_serializer = UserSerializer(instance=request.user, context={
                    'company_id': request.user.company.id
                })

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
        GET: we don't validate the token here, we validate using jwt_required() decorator, we just return a ok response
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
        POST: recieves a json containing the url of the front-end and a email to send a new password 
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
        POST: recieves data com user and company and creates a new company
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def post(self, request):
        serializer = OnboardingSerializer(data=request.data)
        if serializer.is_valid():
            if UserExtended.authentication_.exists_user_by_email(serializer.validated_data['user_email']):
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
        GET: You need to send the refresh token in the header in order to recieve a new token
        and a new refresh token
    """
    def get(self, request):
        jwt = JWT()
        jwt.extract_jwt_from_request(request)
        if jwt.is_valid():
            user = UserExtended.authentication_.user_by_user_id(jwt.data['id'])
            if user and jwt.data['type'] == 'refresh':
                user = UsersService.update_refresh_token_and_user_last_login(user)
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
        POST: Method that recieves the new password and the temp password and changes the user password.
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


class CompanyView(APIView):
    """
    This view is responsible for showing the company data to the user. 
    This is not for settings but instead it is usually used to get basic information about the company.
    This way the front-end or whathever can handle the information as it should. 

    Methods:
        GET: Gets a basic data from an overview about the company. It name, it's id. If it is active or not.
        How many trial days does it have left and so on.
    """
    def get(self, request, company_id):
        instance = Company.authentication_.company_by_company_id(company_id)
        serializer = CompanySerializer(instance=instance)
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UserView(APIView):
    """
    This view is responsible for retrieving user data to the user. When he logs in we send the user data
    but we need it on other ocasions. With this we can get the most updated data whenever he opens the 
    app.

    Methods:
        GET: Returns the user data to the user. This holds all of the user data. Obviously the user
        needs to be logged in to use this.
    """
    def get(self, request, company_id):
        instance = UserExtended.authentication_.user_by_user_id(request.user.id)
        serializer = UserSerializer(instance=instance, context={
            'company_id': company_id
        })
        return Response({
            'status': 'ok',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
class UserVisualizationTypeView(APIView):
    """
    This is responsible for changing and updating the user's visualization types. Visualization types holds what 
    visualization the user is on. Could be `dashboard`, `listing` and `kanban`. We usually use this when the user
    changes the visualization type in the frontend.

    Methods:
        PUT: Changes the visualization type of a user.
    """
    authentication_classes = [CsrfExemptSessionAuthentication]

    def put(self, request, company_id, visualization_type_id):
        UserExtended.authentication_.update_user_visualization_type(request.user.id, visualization_type_id)

        return Response({
            'status': 'ok'
        }, status=status.HTTP_200_OK)