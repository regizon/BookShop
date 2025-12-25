
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem
from cart.serializers import CartItemSerializer, ViewItemsSerializer
from cart.services import get_or_create_cart, get_book


# Create your views here.
class AddItemToCart(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        request = self.request
        cart = get_or_create_cart(request)
        price, cart_item = get_book(serializer, cart)
        if cart_item:
            cart_item.quantity += 1
            cart_item.price += price
            cart_item.save()
        else:
            serializer.save(cart=cart, price=price)

class DeleteFromCart(APIView):
    def delete(self, request):
        cart = get_or_create_cart(request)
        serializer = CartItemSerializer(data = request.data)
        serializer.is_valid()
        price, cart_item = get_book(serializer, cart)
        if cart_item:
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.price -= price
                cart_item.save()
            elif cart_item.quantity == 1:
                cart_item.delete()
        else:
            return Response({"message": "No such book in cart"},status=status.HTTP_404_NOT_FOUND)
        return Response(status.HTTP_200_OK)
class ViewCart(APIView):
    def get(self, request):
        cart = get_or_create_cart(request)
        serializer = ViewItemsSerializer(cart)
        return Response(serializer.data)