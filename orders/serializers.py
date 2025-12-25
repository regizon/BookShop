from rest_framework import serializers

from orders.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_price', 'status', 'order_date', 'items']
        read_only_fields = ['id', 'customer', 'order_date', 'total_price', 'status']