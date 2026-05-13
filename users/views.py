import logging
import os

from django.conf import settings
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from cart.services import get_or_create_cart, merge_carts
from users.brute_force import record_failed_attempt
from users.services import check_login_code, request_login_code, get_tokens_for_user, get_user, register_user

from users.models import EmailLoginCode
from users.serializers import UserRegisterSerializer, EmailVerifySerializer, EmailSerializer, EmailVerifySerializerTest, \
    UserSerializer

auth_logger = logging.getLogger('auth_logger')


def _get_client_ip(request) -> str:
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', 'unknown')


def _get_user_agent(request) -> str:
    return request.META.get('HTTP_USER_AGENT', 'unknown')



def _cookie_kwargs():
    is_prod = os.getenv('DJANGO_ENV') == 'production'
    return {
        'httponly': True,
        'secure': is_prod,
        'samesite': 'Strict' if is_prod else 'Lax',
        'path': '/',
    }


def set_auth_cookies(response, access_token, refresh_token=None):
    kwargs = _cookie_kwargs()
    access_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
    response.set_cookie(
        'access_token',
        str(access_token),
        max_age=int(access_lifetime.total_seconds()),
        **kwargs,
    )
    if refresh_token is not None:
        refresh_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        response.set_cookie(
            'refresh_token',
            str(refresh_token),
            max_age=int(refresh_lifetime.total_seconds()),
            **kwargs,
        )


def clear_auth_cookies(response):
    kwargs = _cookie_kwargs()
    samesite = kwargs['samesite']
    response.delete_cookie('access_token', path='/', samesite=samesite)
    response.delete_cookie('refresh_token', path='/', samesite=samesite)



class RegisterUserRequest(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user_exist = get_user_model().objects.filter(email=email).exists()
        if user_exist:
            return Response({"message": "user already exists"}, status=status.HTTP_400_BAD_REQUEST)

        request_login_code(email)
        return Response({"message": "Code was sent"}, status=status.HTTP_200_OK)


class CheckAdmin(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response(status=status.HTTP_200_OK)


class LoginUserRequest(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data['email']
        if get_user_model().objects.filter(email=email).exists():
            request_login_code(email)
            return Response({"message": "Code was sent"}, status=status.HTTP_200_OK)

        return Response({"message": "User is not exist"}, status=status.HTTP_404_NOT_FOUND)


class EmailVerify(APIView):
    def post(self, request):
        serializer = EmailVerifySerializerTest(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data.get('email')
        code = validated_data.get('code')
        ip = _get_client_ip(request)
        ua = _get_user_agent(request)

        if check_login_code(email, code):
            user = get_user(email)
            if user is None:
                phone_number = validated_data.get('phone_number')
                native_name = validated_data.get('native_name')
                user = register_user(email, native_name, phone_number)

            tokens = get_tokens_for_user(user)
            merge_carts(request, user)

            auth_logger.info(
                'LOGIN_SUCCESS | user_id=%s | ip=%s | user_agent=%s',
                user.id,
                ip,
                ua,
            )

            response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            set_auth_cookies(response, tokens['access'], tokens['refresh'])
            return response

        auth_logger.warning(
            'LOGIN_FAILED | email=%s | ip=%s | user_agent=%s | reason=invalid_or_expired_code',
            email,
            ip,
            ua,
        )
        record_failed_attempt(ip, email)
        return Response({"message": "Помилковий або вже недійсний код"}, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenRefreshView(APIView):

    def post(self, request):
        raw_refresh = request.COOKIES.get('refresh_token')
        ip = _get_client_ip(request)
        if not raw_refresh:
            auth_logger.warning('TOKEN_REFRESH_FAILED | ip=%s | reason=no_refresh_cookie', ip)
            return Response({"message": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(raw_refresh)
            user_id = refresh.get('user_id')
            access_token = str(refresh.access_token)
            auth_logger.info('TOKEN_REFRESH | user_id=%s | ip=%s', user_id, ip)
            response = Response({"message": "Token refreshed"}, status=status.HTTP_200_OK)
            set_auth_cookies(response, access_token)
            return response
        except TokenError as e:
            auth_logger.warning(
                'TOKEN_REFRESH_FAILED | ip=%s | reason=%s',
                ip,
                str(e),
            )
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        ip = _get_client_ip(request)
        user_id = request.user.id if request.user.is_authenticated else 'anonymous'
        auth_logger.info('LOGOUT | user_id=%s | ip=%s', user_id, ip)
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        clear_auth_cookies(response)
        return response


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "email": request.user.email,
            "is_staff": request.user.is_staff,
        }, status=status.HTTP_200_OK)


class UserDetails(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
