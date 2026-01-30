
from rest_framework import status
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import CartItem
from cart.serializers import CartItemRedactorSerializer, ViewItemsSerializer, CartItemViewSerializer
from cart.services import get_or_create_cart, add_item, NotEnoughItemsInStock, NotSuchItemInCart, \
    minus_item, get_cart


# Create your views here.
class AddItemToCart(APIView):
    queryset = CartItem.objects.all()

    def post(self, request):
        serializer = CartItemRedactorSerializer(data=request.data)
        cart = get_or_create_cart(request)
        if serializer.is_valid():
            book = serializer.validated_data['book']

            try:
                add_item(cart, book)

                return Response({
                    "message": "Item added to cart"},
                    status.HTTP_201_CREATED
                )

            except NotEnoughItemsInStock:
                return Response({
                    "message": "Not enough items in stock"
                }, status.HTTP_409_CONFLICT)



class MinusFromCart(APIView):
    def delete(self, request):
        cart = get_or_create_cart(request)
        serializer = CartItemRedactorSerializer(data = request.data)
        if serializer.is_valid():
            try:
                book = serializer.validated_data.get('book')
                minus_item(book, cart)
                return Response(
                    {
                        "message" : "Item deleted from cart",
                    },
                    status.HTTP_200_OK
                )

            except NotSuchItemInCart:
                return Response({
                    "message" : "Item not in cart",
                }, status.HTTP_404_NOT_FOUND)

        else:
            return Response({
                "message" : "Something went wrong",
            }, status.HTTP_400_BAD_REQUEST)

class ViewCart(APIView):
    def get(self, request):
        cart = get_or_create_cart(request)
        serializer = ViewItemsSerializer(cart)
        return Response(serializer.data)


class DeleteFromCart(DestroyAPIView):
    serializer_class = CartItemViewSerializer

    def get_queryset(self):
        cart = get_cart(self.request)
        return CartItem.objects.filter(cart=cart)