from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.services import get_or_create_cart, merge_carts
from users.services import check_login_code, request_login_code, get_tokens_for_user, get_user, register_user

from users.models import EmailLoginCode
from users.serializers import UserRegisterSerializer, EmailVerifySerializer, EmailSerializer, EmailVerifySerializerTest


# Create your views here.

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
            return Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "Помилковий або вже недійсний код"}, status=status.HTTP_400_BAD_REQUEST)
