from django.urls import path
from orders.views import *


urlpatterns = [
    path('create/', CreateOrder.as_view(), name='add'),
    path('list/', OrderList.as_view(), name='list'),
    path('<int:pk>/', OrderDetail.as_view(), name='detail'),
    path('recent/', RecentOrders.as_view(), name='recent'),
    path('update/<int:pk>/', OrderAdminUpdate.as_view(), name='update'),
]