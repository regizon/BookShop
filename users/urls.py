from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from users import views
from users.views import LoginUserRequest

urlpatterns = [
    path('auth/login/', LoginUserRequest.as_view(), name='login_user'),
    path('auth/register/', views.RegisterUserRequest.as_view(), name='register'),
    path('auth/verify/', views.EmailVerify.as_view(), name='email_verify'),
    path('auth/check/', views.CheckAdmin.as_view(), name='check_admin'),
    path('auth/me/', views.MeView.as_view(), name='me'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', views.CookieTokenRefreshView.as_view(), name='token_refresh'),
    # kept for optional token verification by other clients
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('profile/', views.UserDetails.as_view(), name='profile'),
]
