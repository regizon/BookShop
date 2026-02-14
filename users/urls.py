from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

from users import views
from users.views import LoginUserRequest

urlpatterns = [
    #path('api/token/get/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/', LoginUserRequest.as_view(), name="login_user"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', views.RegisterUserRequest.as_view(), name='register'),
    path('auth/verify/', views.EmailVerify.as_view(), name='token_verify'),
]