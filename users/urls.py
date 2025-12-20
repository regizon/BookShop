from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from users import views
from users.views import GenerateCode

urlpatterns = [
    #path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/', GenerateCode.as_view(), name="get_code"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', views.CreateUser.as_view(), name='register'),
    path('auth/verify/', views.EmailVerify.as_view(), name='token_verify'),
]