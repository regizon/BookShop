from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from orders.services import check_user_cart, OrderConfirmationError, fill_order


class CreateOrder(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        try:
            cart = Cart.objects.filter(customer=user).first()
            cart_items = check_user_cart(cart)
            order = serializer.save(customer=user)
            fill_order(order, cart_items)
            cart.delete()

        except OrderConfirmationError as e:
            raise ValidationError(str(e))


class OrderList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

class OrderDetail(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(customer=user)