from django.urls import path
from orders.views import *


urlpatterns = [
    path('create/', CreateOrder.as_view(), name='add'),
    path('list/', OrderList.as_view(), name='list'),
    path('<int:pk>/', OrderDetail.as_view(), name='detail'),
]