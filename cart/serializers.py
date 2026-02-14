from rest_framework import serializers

from books.models import Book
from books.serializers import BookSerializer
from cart.models import Cart, CartItem

class CartItemRedactorSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = CartItem
        fields = ['cart', 'book', 'quantity', 'price']
        read_only_fields = ['cart', 'price']
    extra_kwargs = {
        'cart': {'required': False}
    }

class CartItemViewSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'book', 'quantity', 'price']
        read_only_fields = ['id', 'cart', 'price']
    extra_kwargs = {
        'cart': {'required': False}
    }

class ViewItemsSerializer(serializers.ModelSerializer):
    items = CartItemViewSerializer(source='cartitem_set', many=True)
    class Meta:
        model = Cart
        fields = ['items']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'book', 'quantity']
