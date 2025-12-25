from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services import check_login_code, request_login_code, get_tokens_for_user

from users.models import EmailLoginCode
from users.serializers import UserRegisterSerializer, EmailVerifySerializer, EmailSerializer


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CreateUser(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer

class GenerateCode(APIView):
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data['email']
        if get_user_model().objects.filter(email=email).exists():
            request_login_code(email)
            return Response({"message": "Code was sent"}, status=status.HTTP_200_OK)

        return Response({"message": "User is not exist"}, status=status.HTTP_400_BAD_REQUEST)
class EmailVerify(APIView):

    def post(self, request):
        serializer = EmailVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        email = validated_data.get('email')
        code = validated_data.get('code')

        if check_login_code(email, code):
            user = get_user_model().objects.get(email=email)
            tokens = get_tokens_for_user(user)
            return Response({"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK)

        return Response({"message": "Invalid or expired code"}, status=status.HTTP_417_EXPECTATION_FAILED)
