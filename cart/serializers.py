from rest_framework import serializers

from cart.models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'book', 'quantity', 'price']
        read_only_fields = ['cart', 'price']
    extra_kwargs = {
        'cart': {'required': False}
    }

class ViewItemsSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(source='cartitem_set', many=True)
    class Meta:
        model = Cart
        fields = ['items']


class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart', 'book', 'quantity']
