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
from users.services import check_login_code, request_login_code, get_tokens_for_user, get_user, register_user

from users.models import EmailLoginCode
from users.serializers import UserRegisterSerializer, EmailVerifySerializer, EmailSerializer, EmailVerifySerializerTest, \
    UserSerializer


# ── cookie helpers ────────────────────────────────────────────────────────────

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


# ── views ─────────────────────────────────────────────────────────────────────

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

        if check_login_code(email, code):
            user = get_user(email)
            if user is None:
                phone_number = validated_data.get('phone_number')
                native_name = validated_data.get('native_name')
                user = register_user(email, native_name, phone_number)

            tokens = get_tokens_for_user(user)
            merge_carts(request, user)

            response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            set_auth_cookies(response, tokens['access'], tokens['refresh'])
            return response

        return Response({"message": "Помилковий або вже недійсний код"}, status=status.HTTP_400_BAD_REQUEST)


class CookieTokenRefreshView(APIView):
    """Reads refresh_token cookie, issues a new access_token cookie."""

    def post(self, request):
        raw_refresh = request.COOKIES.get('refresh_token')
        if not raw_refresh:
            return Response({"message": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(raw_refresh)
            access_token = str(refresh.access_token)
            response = Response({"message": "Token refreshed"}, status=status.HTTP_200_OK)
            set_auth_cookies(response, access_token)
            return response
        except TokenError as e:
            return Response({"message": str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        response = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
        clear_auth_cookies(response)
        return response


class MeView(APIView):
    """Returns basic profile for any authenticated user (used to bootstrap frontend auth state)."""
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
