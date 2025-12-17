from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny

from users.serializers import UserRegisterSerializer

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CreateUser(CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserRegisterSerializer
