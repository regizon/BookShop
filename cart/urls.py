from django.urls import path
from cart.views import *


urlpatterns = [
    path('add/', AddItemToCart.as_view(), name='add'),
    path('view/', ViewCart.as_view(), name='view'),
    path('delete/', MinusFromCart.as_view(), name='delete'),
    path('delete/<int:pk>', DeleteFromCart.as_view(), name='delete'),
]