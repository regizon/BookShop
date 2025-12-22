from django.urls import path
from cart.views import *


urlpatterns = [
    path('add/', AddItemToCart.as_view(), name='add'),
    path('view/', ViewCart.as_view(), name='view'),
    path('delete/', DeleteFromCart.as_view(), name='delete'),
]