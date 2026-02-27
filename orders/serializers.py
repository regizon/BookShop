from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from orders.models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'item', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    city = serializers.CharField(required=False)
    street = serializers.CharField(required=False)
    house = serializers.CharField(required=False)
    apartment = serializers.CharField(required=False)

    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_price', 'status', 'order_date', 'items', 'name', 'surname', 'comments', 'delivery_type', 'payment_method',
                   'city', 'street', 'house', 'apartment']
        read_only_fields = ['id', 'customer', 'order_date', 'total_price', 'status']

    def validate(self, data):
        if data['delivery_type'] == 'courier':
            if 'street' not in data:
                raise ValidationError({'street': "Необхідно вказати вулицю при виборі кур'єрскої доставки"})
            elif 'city' not in data:
                raise ValidationError({'city': "Необхідно вказати місто при виборі кур'єрскої доставки"})
            elif 'house' not in data:
                raise ValidationError({'house': "Необхідно вказати номер будинку при виборі кур'єрскої доставки"})
            elif 'apartment' not in data:
                raise ValidationError({'apartment': "Необхідно вказати квартиру при виборі кур'єрскої доставки"})
        return data