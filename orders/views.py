from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED

from cart.models import Cart, CartItem
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer


class CreateOrder(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        user = self.request.user
        cart = Cart.objects.filter(customer=user).first()
        if cart is None:
            raise ValidationError({"cart": "Cart does not exist."})
        cart_items = CartItem.objects.filter(cart=cart)
        if len(cart_items) == 0:
            raise ValidationError({"cart": "Cart is empty"})

        order = serializer.save(customer=user)
        for item in cart_items:
            book = item.book
            price = item.price
            quantity = item.quantity
            order_item = OrderItem.objects.create(order=order, item=book, price=price, quantity=quantity)
            order.total_price += price * quantity
            order_item.save()
            order.save()
        cart_items.delete()


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